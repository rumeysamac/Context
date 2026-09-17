
import sys
import os

class BaglamSikistirmaYonetici:
   
 
    # Basit stop-words (durak kelimeler) listesi 
    STOP_WORDS = {"ve", "veya", "ile", "bir", "bu", "şu", "da", "de", "için", "yani", "gibi"}

    def __init__(self, dosya_adi: str = "compressed_context.txt", max_mesaj: int = 3, max_karakter: int = 100):
        self.dosya_adi = dosya_adi
        self.max_mesaj = max_mesaj
        self.max_karakter = max_karakter
        self.mesaj_gecmisi = []
        self.dosya = None
        print(f"1. [__init__] Bağlam Sıkıştırıcı ilklendirildi. (Max Mesaj: {max_mesaj}, Max Kr: {max_karakter})")

    def __enter__(self):
        """ContextManager girişi: Kaynak ayrılır."""
        print(f"2. [__enter__] Sıkıştırılmış bağlam dosyası hazırlanıyor: '{self.dosya_adi}'")
        self.dosya = open(self.dosya_adi, "w", encoding="utf-8")
        return self  # 'with ... as manager' kullanımı için self döndürülür

    def _metni_temizle_ve_sikistir(self, metin: str) -> str:
        """
        Girdi metnindeki gereksiz boşlukları ve durak kelimeleri temizler.
        """
        # 1. Fazla boşlukları ve satır başlarını teke indir
        kelimeler = metin.split()
        
        # 2. Stop-words (durak kelimeler) filtrelemesi (küçük harfe çevirerek bakılır)
        sadelestirilmis = [k for k in kelimeler if k.lower() not in self.STOP_WORDS]
        
        yeni_metin = " ".join(sadelestirilmis)
        
        # 3. Budama (Pruning): Karakter sınırı aşılıyorsa kes
        if len(yeni_metin) > self.max_karakter:
            yeni_metin = yeni_metin[:self.max_karakter].rstrip() + "... [BUDANDI]"
            
        return yeni_metin

    def mesaj_ekle(self, rol: str, icerik: str):
        """
        Yeni bir diyalog mesajını alır, sıkıştırır ve kayan pencere (sliding window)
        yöntemiyle geçmişe ekler.
        """
        ham_boyut = len(icerik)
        sikistirilmis_icerik = self._metni_temizle_ve_sikistir(icerik)
        sıkışmış_boyut = len(sikistirilmis_icerik)
        
        # Sıkıştırılmış mesajı kaydet
        yeni_mesaj = f"[{rol.upper()}]: {sikistirilmis_icerik}"
        self.mesaj_gecmisi.append(yeni_mesaj)
        
        print(f"  -> [{rol}] Mesajı Sıkıştırıldı: {ham_boyut} kr -> {sıkışmış_boyut} kr (Tasarruf: %{100 - (sıkışmış_boyut/ham_boyut*100):.1f})")

        # Kayan Pencere (Sliding Window): Eskiyen mesajları otomatik sil/arşivle
        if len(self.mesaj_gecmisi) > self.max_mesaj:
            atilan = self.mesaj_gecmisi.pop(0)
            print(f"  [PENCERE KAYDI] Eski mesaj bellekten çıkarıldı: '{atilan[:30]}...'")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        ContextManager çıkışı: Tüm sıkıştırılmış bağlam geçmişi dosyaya yazılır
        ve kaynak kapatılır.
        """
        print("\n4. [__exit__] Sıkıştırılmış bağlam kaydediliyor ve kaynaklar temizleniyor...")
        
        if self.dosya and not self.dosya.closed:
            self.dosya.write("=== SIKIŞTIRILMIŞ BAĞLAM GEÇMİŞİ ===\n")
            for msg in self.mesaj_gecmisi:
                self.dosya.write(msg + "\n")
            
            self.dosya.close()
            print(f"  -> Dosya kapatıldı: '{self.dosya_adi}'")

        # Hata kontrolü
        if exc_type is not None:
            print(f"  [HATA YÖNETİMİ] Hata tespit edildi: {exc_val}")
            # False dönerek hatayı yukarı fırlatmaya izin veriyoruz
            return False
            
        return True


# ==========================================
# TEST VE KULLANIM ÖRNEĞİ
# ==========================================
print("--- BAĞLAM SIKIŞTIRMA TESTİ BAŞLIYOR ---\n")

uzun_metin_1 = "Merhaba bu ve şu ürünler için bir adet destek bileti oluşturmak istiyorum ancak sistem hata veriyor."
uzun_metin_2 = "Sistemdeki hata veritabanı bağlantı zaman aşımı ile ilgili yani sunucu yanıt vermiyor gibi görünüyor."
uzun_metin_3 = "Lütfen bu sorunu en kısa sürede çözebilir misiniz çünkü acil bir durum söz konusu."
uzun_metin_4 = "Tamam harika, ilginiz ve yardımınız için çok teşekkür ederim iyi çalışmalar dilerim."

with BaglamSikistirmaYonetici(dosya_adi="ai_context.txt", max_mesaj=3, max_karakter=60) as baglam:
    print("\n3. [WITH BLOĞU] Mesajlar bağlama gönderiliyor...\n")
    
    baglam.mesaj_ekle("User", uzun_metin_1)
    baglam.mesaj_ekle("System", uzun_metin_2)
    baglam.mesaj_ekle("User", uzun_metin_3)
    
    # Bu mesaj eklendiğinde ilk mesaj (Sliding Window) elenecektir
    baglam.mesaj_ekle("User", uzun_metin_4)

print("\n--- TEST BİTTİ ---")

# Oluşturulan dosyanın içeriğini okuyup ekrana yazdıralım
if os.path.exists("ai_context.txt"):
    print("\n--- 'ai_context.txt' İÇERİĞİ ---")
    with open("ai_context.txt", "r", encoding="utf-8") as f:
        print(f.read())