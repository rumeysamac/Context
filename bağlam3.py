# DURUM VE BELLEK BAĞLAMI
import json
import time


class Mesaj:

    def __init__(self, rol: str, icerik: str):
        self.rol = rol
        self.icerik = icerik
        self.zaman = time.strftime("%H:%M:%S")

    def to_dict(self):
        return {"rol": self.rol, "icerik": self.icerik, "zaman": self.zaman}

class DurumBaglami:

    def __init__(self, oturum_id: str, maks_bellek_sayisi: int = 3 ):
        self.oturum_id = oturum_id
        self.maks_bellek_sayisi = maks_bellek_sayisi
        self._sistem_talimati = ""
        self._gecmis = []

    def sistem_talimati_ekle(self, talimat: str):
        self._sistem_talimati = talimat

    def olay_ekle(self, rol: str, icerik: str):
        yeni_mesaj = Mesaj(rol, icerik)
        self._gecmis.append(yeni_mesaj) 

    def aktif_hafizayi_derle(self):
        son_mesajlar = self._gecmis[-self.maks_bellek_sayisi:]

        return{
            "oturum_id": self.oturum_id,
            "sistem_talimati": self._sistem_talimati,
            "aktif_hafiza": [m.to_dict() for m in son_mesajlar],
            "toplam_gecmis_olay_sayisi": len(self._gecmis),
        }

    def baglami_json_kaydet(self, dosya_adi: str = "oturum_baglami.json"):
        veri = {
            "oturum_id": self.oturum_id,
            "sistem_talimati": self._sistem_talimati,
            "gecmis": [m.to_dict() for m in self._gecmis],
        }

        with open(dosya_adi, "w", encoding="utf-8") as f:
           json.dump(veri, f, ensure_ascii=False, indent=4)
        print(f"\n Bağlam '{dosya_adi}' dosyasına kaydedildi")

oturum = DurumBaglami(oturum_id="oturum_8899", maks_bellek_sayisi=2)
oturum.olay_ekle("user", "Selam, ben Rümeysa.")
oturum.olay_ekle("asisstant", "Selam Rümeysa!")
oturum.olay_ekle("user", "Python öğreniyorum.")

aktif_baglam = oturum.aktif_hafizayi_derle()

print("\n--- Aktif Hafıza (Son 2 Mesaj) ---")
for m in aktif_baglam["aktif_hafiza"]:
    print(f"[{m['zaman']}]  {m['rol'].upper()}: {m['icerik']}")
