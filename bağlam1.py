# KAYNAK YÖNETİMİ YAPISI
import sys
import time

class DosyaYonetici:
    def __init__(self, dosya_adi: str, mod: str = "r"):
        """
        1. Adım: Nesne ilklendirilir.
        Burada henüz kaynak AÇILMAZ, sadece parametreler saklanır.
        """
        self.dosya_adi = dosya_adi
        self.mod = mod
        self.dosya_nesnesi = None
        print(f"1. [__init__] '{self.dosya_adi}' için yönetici oluşturuldu.")

    def __enter__(self):
        """
        2. Adım: 'with' bloğunun içine girildiği an çalışır.
        Gerçek kaynak ayırma işlemi burada yapılır. 
        """
        print(f"2. [__enter__] '{self.dosya_adi}' dosyası açılıyor...")
        self.dosya_nesnesi = open(self.dosya_adi, self.mod, encoding="utf-8")
     
        
        return self.dosya_nesnesi

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        3. Adım: 'with' bloğundan çıkılırken (normal veya hatalı) çalışır.
        Temizlik işlemi burada garanti altına alınır.
        """
        print("\n4. [__exit__] Bloktan çıkılıyor, temizlik başlatıldı...")

        
        if self.dosya_nesnesi and not self.dosya_nesnesi.closed: 
            self.dosya_nesnesi.close()
            print(f"   -> '{self.dosya_adi}' dosyası başarıyla kapatıldı.")

      
        if exc_type is not None:
            print(f"  Hata yakalandı!")
            print(f"  -Hata Türü   : {exc_type.__name__}")
            print(f"  -Hata Mesajı : {exc_val}")

             
            if exc_type is ZeroDivisionError:
                print("   -> 'ZeroDivisionError' hatası yutuldu! Program çalışmaya devam edicel.")
                return True # Hatayı dışarı fırlatma

        
        return False



print("--- TEST 1 BAŞLIYOR ---")
with DosyaYonetici("test.txt", "w") as f:
    print("3. [WITH BLOĞU] Dosyaya veri yazılıyor...")
    f.write("Saf Python ile kaynak yönetimi harika çalışıyor'\n")

print("-- TEST 2 BAŞLIYOR (Hata Durumu) ---")
try:
    with DosyaYonetici("test.txt", "a") as f:
        print("3. [WITH BLOĞU] Dosyaya ekleme yapılıyor...")
        f.write("Yeni satır...\n")

        print("3. [WITH BLOĞU] Sıfıra bölme hatası tetikleniyor...")     
        sonuc = 10 / 0 

except ZeroDivisionError:
    print("X. Bu mesaj HİÇBİR ZAMAN görünmeyecek çünkü ___exit__ hatayı yuttu.")

print("--- TEST 2 BİTTİ (Hata yutulduğu için program buraya ulaştı) ---")             