#THREAD VE ASYNC GÜVENLİ BAĞLAM
import asyncio
from contextvars import ContextVar

oturum_kullanici: ContextVar[str] = ContextVar("oturum_kullanici", default="Misafir")
oturum_id: ContextVar[int] = ContextVar("oturum_id", default=0)

async def veritabani_sorgusu_calistir():
    """
    Bu fonksiyon Dışarıdan hiçbir parametre almaz!
    Buna rağmen hangi kullanıcının isteğini işlediğni doğrudan bağlamdan okur.
    """

    mevcut_kullanici = oturum_kullanici.get()
    mevcut_id = oturum_id.get()

    print(f"  -->  [DB Sorgusu] Çalışan Oturum ID: {mevcut_id} | Kullanıcı: {mevcut_kullanici}")

async def istek_isle(kullanici_adi: str, istek_id: int):
    """Her yeni kullanıcı isteği geldiğinde çalışan ana asenkron görev."""

    # 2.BAĞLAM DEĞER ATAMA (.set)
    token_kullanici = oturum_kullanici.set(kullanici_adi)
    token_id = oturum_id.set(istek_id)

    print(f"[BAŞLADI] İstek alındı: {kullanici_adi} (ID: {istek_id})")

    await asyncio.sleep(1)

    await veritabani_sorgusu_calistir()

#temizleme kısmı
    oturum_kullanici.reset(token_kullanici)
    oturum_id.reset(token_id)

    print(f"[TAMAMLANDI] İstek bitti: {kullanici_adi}\n")

async def main():
    print("--- EŞZAMANLI İSTEKLER BAŞLIYOR ---\n")
    await asyncio.gather(
        istek_isle("Ahmet", 101),
        istek_isle("Ayşe", 102)
    )

asyncio.run(main())    

