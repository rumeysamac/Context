import json
import time
from typing import Dict, List, Optional, Any


class Mesaj :
    def __init__(self, rol: str, icerik: str, zaman: Optional[str] = None):
        self.rol = rol.lower().strip()
        self.icerik = icerik
        self.zaman = zaman or time.strftime("%H:%M:%S")

    def to_dict(self) -> Dict[str, str]:
        return {
            "rol": self.rol,
            "icerik": self.icerik,
            "zaman": self.zaman
        }
    @classmethod
    def from_dict(cls, veri: Dict[str, str]) -> "Mesaj":
        return cls(
           rol=veri["rol"],
           icerik=veri["icerik"],
           zaman=veri.get("zaman")
        )   

class DurumBaglami:
    def __init__(self, oturum_id: str, maks_bellek_sayisi: int = 3):
        self.oturum_id = oturum_id
        self.maks_bellek_sayisi = maks_bellek_sayisi
        self._sistem_talimati = ""
        self._gecmis: List[Mesaj] = []
        self._ozetlenmis_bellek = ""  

    def olay_ekle(self, rol: str, icerik: str) -> None:
        yeni_mesaj = Mesaj(rol=rol, icerik=icerik)
        self._gecmis.append(yeni_mesaj)     


    def sistem_talimati_ekle(self, talimat: str) -> None:
        self._sistem_talimati = talimat.strip()

    def olay_ekle(self, rol: str, icerik: str) -> None:
        yeni_mesaj = Mesaj(rol=rol, icerik=icerik)
        self._gecmis.append(yeni_mesaj)    


    def aktif_hafizayi_derle(self) -> Dict[str, Any]:

        aktif_mesajlar = self._gecmis[-self.maks_bellek_sayisi:]
        eski_mesajlar = self._gecmis[:-self.maks_bellek_sayisi] if len(self._gecmis) > self.maks_bellek_sayisi else []

        if eski_mesajlar:
            ozet_satirlari = [f"- {m.rol.upper()} [{m.zaman}]: {m.icerik}" for m in eski_mesajlar]
            self._ozetlenmis_bellek = "\n".join(ozet_satirlari)

        return {
            "oturum_id": self.oturum_id,
            "sistem_talimati": self._sistem_talimati,
            "gecmis_ozeti": self._ozetlenmis_bellek,  # Uzun süreli hafıza
            "aktif_hafiza": [m.to_dict() for m in aktif_mesajlar],  # Kısa süreli hafıza
            "toplam_mesaj_sayisi": len(self._gecmis)
        }

    def baglami_json_kaydet(self, dosya_adi: str = "oturum_baglami.json") -> None:
        """Mevcut oturum durumunu ve tüm geçmişi diske JSON formatında kaydeder."""
        # 1. Bütün sınıf durumunu JSON'ın anlayacağı bir sözlük yapısına dönüştürüyoruz
        veri = {
            "oturum_id": self.oturum_id,
            "sistem_talimati": self._sistem_talimati,
            "ozetlenmis_bellek": self._ozetlenmis_bellek,
            # Bütün geçmiş mesaj nesnelerini sözlüğe çeviriyoruz
            "gecmis": [m.to_dict() for m in self._gecmis]
        }
        
        # 2. Dosyayı yazma ('w') modunda, Türkçe karakter desteğiyle açıp yazıyoruz
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=4)
            
        print(f"[LOG] Oturum durumu '{dosya_adi}' dosyasına kaydedildi.")

    @classmethod
    def json_dan_yukle(cls, dosya_adi: str = "oturum_baglami.json", maks_bellek_sayisi: int = 3) -> "DurumBaglami":
        """Diskteki JSON dosyasından oturum durumunu okur ve yeni bir DurumBaglami nesnesi döndürür."""
        # 1. JSON dosyasını okuma ('r') modunda açıp sözlüğe dönüştürüyoruz
        with open(dosya_adi, "r", encoding="utf-8") as f:
            veri = json.load(f)

        # 2. Sınıfın kendisinden (cls = DurumBaglami) yeni bir nesne örneği oluşturuyoruz
        oturum = cls(oturum_id=veri["oturum_id"], maks_bellek_sayisi=maks_bellek_sayisi)
        
        # 3. Diskteki kayıtlı durumları yeni nesnemize yüklüyoruz
        oturum._sistem_talimati = veri.get("sistem_talimati", "")
        oturum._ozetlenmis_bellek = veri.get("ozetlenmis_bellek", "")
        
        # 4. JSON'daki ham sözlük geçmişini tekrar Mesaj nesnelerine çevirip yüklüyoruz
        oturum._gecmis = [Mesaj.from_dict(m) for m in veri.get("gecmis", [])]

        print(f"[LOG] '{dosya_adi}' dosyasından oturum yüklendi. (Toplam {len(oturum._gecmis)} mesaj)")
        return oturum
    # --- TEST VE KULLANIM ALANI ---
if __name__ == "__main__":
    # 1. Oturumu Başlatıyoruz
    oturum = DurumBaglami(oturum_id="oturum_8899", maks_bellek_sayisi=2)
    oturum.sistem_talimati_ekle("Sen yardımsever bir AI asistanısın.")

    # 2. Örnek Mesajlar Ekiyoruz
    oturum.olay_ekle("user", "Selam, ben Rümeysa.")
    oturum.olay_ekle("assistant", "Selam Rümeysa! Nasıl yardımcı olabilirim?")
    oturum.olay_ekle("user", "Python ile durum yönetimini öğreniyorum.")

    # 3. Aktif Hafızayı Derleyip Ekrana Yazdırıyoruz
    aktif_baglam = oturum.aktif_hafizayi_derle()

    print("\n=== AKTİF HAFIZA VE DURUM BİLGİSİ ===")
    print("Sistem Talimatı :", aktif_baglam["sistem_talimati"])
    print("Geçmiş Özeti   :\n", aktif_baglam["gecmis_ozeti"])
    print("Aktif Mesajlar :", aktif_baglam["aktif_hafiza"])

    # 4. JSON Olarak Diske Kaydet
    oturum.baglami_json_kaydet("oturum_baglami.json")