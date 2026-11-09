import time
import sys
import random
from typing import Sequence


class Oyunfonksiyonlari:
    
    def yavas_yazdir(self, metin: str, gecikme: float = 0.02) -> None:
        for karakter in metin:
            sys.stdout.write(karakter)
            sys.stdout.flush()
            time.sleep(gecikme)
        print()

    def yukleniyor(self) -> None:
        print("\n")
        mesaj_durumlari = [
            "Sistem Başlatılıyor    ",
            "Sistem Başlatılıyor.   ",
            "Sistem Başlatılıyor..  ",
            "Sistem Başlatılıyor... "
        ]
        for _ in range(3):
            for mesaj in mesaj_durumlari:
                sys.stdout.write('\r' + mesaj)
                sys.stdout.flush()
                time.sleep(0.3)
        print("\n")

    def baslangic_ekrani(self) -> None:
        self.yukleniyor()
        print("="*100)
        print("\n")
        baslik = [
            "  BBBB      IIIIIII    TTTTTTTT       Y   Y      OOOO      L         U     U",
            "  B   B       III         TT           Y Y      O    O     L         U     U",
            "  BBBB        III         TT            Y       O    O     L         U     U",
            "  B   B       III         TT            Y       O    O     L         U     U",
            "  BBBB      IIIIIII       TT            Y        OOOO      LLLLLL     UUUUU "
        ]
        for satir in baslik:
            print(satir)
            time.sleep(0.1)
        print("\n")
        print("="*100)
        self.yavas_yazdir(">>> SİBER SAVAŞ BAŞLIYOR...", 0.05)
        time.sleep(1)


class DijitalVarlik:
    
    def __init__(self, ad: str, guc: int, can: int) -> None:
        self.ad = ad
        self.guc = guc
        self.can = can
        self.max_can = can

    def canli_mi(self) -> bool:
        return self.can > 0

    def hasar_al(self, miktar: int) -> None:
        self.can -= miktar
        if self.can < 0: self.can = 0
        print(f"   -> {self.ad} {miktar} veri hasarı aldı! (Kalan can(HP): {self.can})")


class SiberSavasci(DijitalVarlik):
    def __init__(self, ad: str, guc: int, can: int, sinif_adi: str) -> None:
        super().__init__(ad, guc, can)
        self.sinif_adi = sinif_adi
        self.ozel_guc_hakki = 5

    def saldir(self, dusman: DijitalVarlik) -> None:
        print(f"\n⚔️  {self.ad} saldırıyor!")
        dusman.hasar_al(self.guc)

    def savunma_yap(self) -> bool:
        print(f"\n🛡️  {self.ad} Firewall açtı! (Gelen hasar azalacak)")
        return True

    def ozel_guc(self, dusman: DijitalVarlik) -> None:
        pass

class KodAvcisi(SiberSavasci):
    def __init__(self, ad: str) -> None:
        super().__init__(ad, guc=40, can=80, sinif_adi="Kod Avcısı")

    def ozel_guc(self, dusman: DijitalVarlik) -> None:
        if self.ozel_guc_hakki > 0:
            print(f"\n🔥 {self.ad} 'OVERCLOCK' modunu açtı! Çift hasar!")
            dusman.hasar_al(self.guc * 2)
            self.ozel_guc_hakki -= 1
            print(f"   (Kalan Özel Güç Hakkı: {self.ozel_guc_hakki})")
        else:
            print("\n❌ Özel güç hakkın bitti!")

class AgFedaisi(SiberSavasci):
    def __init__(self, ad: str) -> None:
        super().__init__(ad, guc=25, can=120, sinif_adi="Ağ Fedaisi")
    
    def ozel_guc(self, dusman):
        if self.ozel_guc_hakki > 0:
            print(f"\n💉 {self.ad} 'YAMA (PATCH)' uyguladı! Can yenileniyor.")
            self.can += 40
            if self.can > self.max_can: self.can = self.max_can
            print(f"   -> Can yenilendi: {self.can}/{self.max_can}")
            self.ozel_guc_hakki -= 1
            print(f"   (Kalan Özel Güç Hakkı: {self.ozel_guc_hakki})")
        else:
            print("\n❌ Özel güç hakkın bitti!")


class Virus(DijitalVarlik):
    def saldir(self, oyuncu: SiberSavasci, oyuncu_savunmada_mi: bool) -> None:
        hasar = self.guc
        print(f"\n👾 {self.ad} sana zararlı kod yolladı!")
        
        if oyuncu_savunmada_mi:
            print("   -> Firewall sayesinde hasarı blokladın!")
            hasar = hasar // 3 
            
        oyuncu.hasar_al(hasar)



def zorunlu_metin_al(mesaj: str) -> str:
    """Ask until the user enters a non-empty text value."""
    while True:
        deger = input(mesaj).strip()
        if deger:
            return deger
        print("Bu alan boş bırakılamaz.")


def menu_secimi_al(secenekler: Sequence[str], mesaj: str) -> str:
    """Return a normalized menu choice, repeating the prompt on invalid input."""
    secenekler = tuple(secenek.lower() for secenek in secenekler)
    while True:
        secim = input(mesaj).strip().lower()
        if secim in secenekler:
            return secim
        print("Geçersiz seçim. Lütfen tekrar deneyin.")


def karakter_olustur() -> SiberSavasci:
    print("=" * 29)
    print("\n--- KARAKTER SEÇİM EKRANI ---")
    ad = zorunlu_metin_al("Kullanıcı Adınızı Girin: ")
    while True:
        print("\n[1] KOD AVCISI (Yüksek Hasar(40) / Düşük Can(80) / Overclock Özelliği(2x Hasar))")
        print("[2] AĞ FEDAİSİ (Düşük Hasar(25) / Yüksek Can(120) / Patch Özelliği(40 HP Can Yenileme))")
        secim = menu_secimi_al(("1", "2"), "Seçiminiz (1-2): ")

        if secim == "1":
            return KodAvcisi(ad)
        return AgFedaisi(ad)


def rastgele_dusman_uret(seviye_zorlugu: int) -> Virus:
    
    guc_carpan = 1 + (seviye_zorlugu * 0.1)
    
    turler = [
        ("Acemi Script Kiddie", 10, 40),
        ("Trojan.Win32", 15, 60),
        ("Solucan (Worm)", 20, 80),
        ("Spyware Ajanı", 25, 90)
    ]
    
    if seviye_zorlugu % 5 == 0:
        return Virus("💀 FIDYE YAZILIMI (BOSS) 💀", int(35 * guc_carpan), int(150 * guc_carpan))
    
    isim, temel_guc, temel_can = random.choice(turler)
    return Virus(isim, int(temel_guc * guc_carpan), int(temel_can * guc_carpan))

def savas_dongusu(oyuncu: SiberSavasci, dusman: Virus) -> bool:
    oyun = Oyunfonksiyonlari()
    oyun.yavas_yazdir(f"\n⚠️  UYARI: {dusman.ad} tespit edildi! Saldırı başlıyor!", 0.03)
    
    while oyuncu.canli_mi() and dusman.canli_mi():
        print("-"*50)
        oyun.yavas_yazdir(f"\n--- {oyuncu.ad} [{oyuncu.can} HP] vs {dusman.ad} [{dusman.can} HP] ---")
        oyun.yavas_yazdir("1. Saldır  |  2. Savun  |  3. Özel Güç")
        
        hamle = menu_secimi_al(("1", "2", "3"), "Komut Satırı > ")
        savunma = False
        
        if hamle == "1":
            oyuncu.saldir(dusman)
        elif hamle == "2":
            savunma = oyuncu.savunma_yap()
        elif hamle == "3":
            oyuncu.ozel_guc(dusman)
        
        if dusman.canli_mi():
            time.sleep(0.8)
            dusman.saldir(oyuncu, savunma)
        else:
            print(f"\n🏆 TEBRİKLER! {dusman.ad} sistemden silindi.")
            return True 

    if not oyuncu.canli_mi():
        print("\n💀 KRİTİK HATA: SİSTEM ÇÖKTÜ...")
        return False




def main() -> None:
    oyun = Oyunfonksiyonlari()
    oyun.baslangic_ekrani()
        
    oyuncu = karakter_olustur()
    print(f"\nHoş geldin {oyuncu.ad}. Bit Yolu seni bekliyor...")
        
    seviye = 1
        
    while True:
        print(f"\n" + "#"*16)
        print(f"### SEVİYE {seviye} ###")
        print("#"*16)
            
        dusman = rastgele_dusman_uret(seviye)
        sonuc = savas_dongusu(oyuncu, dusman)
            
        if not sonuc:
            print("\nOyun Bitti. Tekrar dene!")
            break
                

        print(f"\nSeviye {seviye} tamamlandı. Veri can(HP) onarılıyor...")
        oyuncu.can += 25
        if oyuncu.can > oyuncu.max_can: oyuncu.can = oyuncu.max_can
        print(f"Güncel Can: {oyuncu.can}")
        
        devam = menu_secimi_al(("e", "h"), "\nBir sonraki sektöre geçilsin mi? (e/h): ")
        if devam != 'e':
            print(f"\nOyundan çıkılıyor. Ulaşılan son seviye: {seviye}")
            break
            
        seviye += 1


if __name__ == "__main__":
    main()
