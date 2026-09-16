import os 
# DOSYA OLUŞTURMA
dosya_adi = "uzun_hikaye.txt"

with open(dosya_adi, "w", encoding="utf-8") as f:
    for i in range(1,13):
        f.write(f"Paragraf {i}: Bu paragraf uzun bağlam işleme sisteminin {i}. konusunu anlatmaktadır. ")
        f.write("Sistem bellek dostu bir yapıda çalışmalı ve bağlamı korumalıdır. \n\n")

    print(f"'{dosya_adi}' dosyası başarıyla oluşturuldu.\n") 


# UZUN BAĞLAM İŞLEYİCİ
def tam_baglam_isleyici(dosya_yolu, max_karakter=250, cakisma_karakter=50):
    
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        metin = f.read()

    # ANLAMSAL SINIR
    paragraflar = metin.split("\n\n")

    # GEÇMİŞ HAFIZA (CONTEXT MEMORY)
    gecmis_hafiza = "Henüz işlenmiş bir geçmiş yok."
    tampon_metin = ""

    for paragraf in paragraflar:
        if not paragraf.strip():
            continue

        if tampon_metin:
            tampon_metin += "\n\n" + paragraf
        else:
            tampon_metin = paragraf

        # Tampon belirlenen maksimum karakter boyutuna ulaştı mı?
        if len(tampon_metin) >= max_karakter:

            isleme_paketi = {
                "hafiza": gecmis_hafiza,
                "mevcut_metin": tampon_metin
            }        
            yield isleme_paketi

            # GEÇMİŞ HAFIZA GÜNCELLEME 
            gecmis_hafiza = f"Son işlenen blok boyutu: {len(tampon_metin)} kr. (Özet: {tampon_metin[:40]}...)"


            # ÇAKIŞMA (OVERLAP) UYGULAMA
            tampon_metin = tampon_metin[-cakisma_karakter:]

    # DÖNGÜ BİTTİĞİNDE ELDE KALAN SON PARÇAYI İŞLE 
    if tampon_metin.strip():
        isleme_paketi = {
            "hafiza": gecmis_hafiza,
            "mevcut_metin": tampon_metin
        }        
        yield isleme_paketi

# MİMARİYİ ÇALIŞTIRMA VE EKRANA BASMA
parca_no = 1
for paket in tam_baglam_isleyici(dosya_adi, max_karakter=250, cakisma_karakter=50):
    print(f"==== PARÇA {parca_no} ====")
    print(f"[GEÇMİŞ HAFIZA (CONTEXT MEMORY)]:\n -> {paket['hafiza']}\n")
    print("=" * 45 + "\n")

    parca_no += 1        