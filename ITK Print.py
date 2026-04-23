
class Dokumen:
    def __init__(self, nama_file: str, jumlah_halaman: int):
        self.nama_file = nama_file
        self.__jumlah_halaman = jumlah_halaman

    def get_jumlah_halaman(self) -> int:
        return self.__jumlah_halaman


class MesinPrint:
    KAPASITAS_MAX_KERTAS = 100
    KAPASITAS_MAX_TINTA  = 100
    BATAS_PERINGATAN     = 20

    def __init__(self, id_mesin: str, stok_kertas: int, stok_tinta: int):
        self.id_mesin      = id_mesin
        self.__stok_kertas = stok_kertas
        self.__stok_tinta  = stok_tinta
        self.__total_cetak = 0

    def get_stok_kertas(self)  -> int: return self.__stok_kertas
    def get_stok_tinta(self)   -> int: return self.__stok_tinta
    def get_total_cetak(self)  -> int: return self.__total_cetak

    def cek_mesin_siap(self) -> bool:
        return self.__stok_kertas > 0 and self.__stok_tinta > 0

    def stok_habis(self) -> bool:
        return self.__stok_kertas == 0 or self.__stok_tinta == 0

    def stok_cukup_untuk(self, halaman: int) -> bool:
        return self.__stok_kertas >= halaman and self.__stok_tinta >= halaman

    def cek_peringatan(self):
        if 0 < self.__stok_kertas <= self.BATAS_PERINGATAN:
            print(f"  *** Kertas hampir habis! Sisa {self.__stok_kertas} lembar.")
        if 0 < self.__stok_tinta <= self.BATAS_PERINGATAN:
            print(f"  *** Tinta hampir habis! Sisa {self.__stok_tinta} unit.")

    def kurangi_stok(self, halaman: int):
        self.__stok_kertas -= halaman
        self.__stok_tinta  -= halaman
        self.__total_cetak += halaman

    def restock(self, tambah_kertas: int = 0, tambah_tinta: int = 0):
        print("\n" + "="*55)
        print(f"  RESTOCK MESIN {self.id_mesin}")
        print("-"*55)

        if tambah_kertas > 0:
            sebelum = self.__stok_kertas
            maks    = self.KAPASITAS_MAX_KERTAS
            if sebelum >= maks:
                print(f"  Kertas sudah penuh ({sebelum}/{maks}).")
            else:
                aktual = min(tambah_kertas, maks - sebelum)
                self.__stok_kertas += aktual
                print(f"  Kertas : {sebelum} + {aktual} = {self.__stok_kertas} lembar")
                if aktual < tambah_kertas:
                    print(f"            (dibatasi kapasitas maks {maks})")

        if tambah_tinta > 0:
            sebelum = self.__stok_tinta
            maks    = self.KAPASITAS_MAX_TINTA
            if sebelum >= maks:
                print(f"  Tinta  sudah penuh ({sebelum}/{maks}).")
            else:
                aktual = min(tambah_tinta, maks - sebelum)
                self.__stok_tinta += aktual
                print(f"  Tinta  : {sebelum} + {aktual} = {self.__stok_tinta} unit")
                if aktual < tambah_tinta:
                    print(f"            (dibatasi kapasitas maks {maks})")

        print("="*55)

    def status_bar(self) -> str:
        bk = self.__buat_bar(self.__stok_kertas, self.KAPASITAS_MAX_KERTAS)
        bt = self.__buat_bar(self.__stok_tinta,  self.KAPASITAS_MAX_TINTA)
        return (
            f"  Mesin       : {self.id_mesin}\n"
            f"  Kertas      : {bk} {self.__stok_kertas}/{self.KAPASITAS_MAX_KERTAS}\n"
            f"  Tinta       : {bt} {self.__stok_tinta}/{self.KAPASITAS_MAX_TINTA}\n"
            f"  Total cetak : {self.__total_cetak} halaman"
        )

    def __buat_bar(self, nilai: int, maks: int, panjang: int = 15) -> str:
        isi = round((nilai / maks) * panjang) if maks > 0 else 0
        return "[" + "#" * isi + "." * (panjang - isi) + "]"


class Pelanggan:
    def __init__(self, nama: str, saldo: float):
        self.nama    = nama
        self.__saldo = saldo

    def get_saldo(self) -> float:
        return self.__saldo

    def potong_saldo(self, jumlah: float):
        self.__saldo -= jumlah

    def cetak_dokumen(self, dokumen: Dokumen, mesin: MesinPrint,
                      harga_per_lembar: float) -> str:
        halaman     = dokumen.get_jumlah_halaman()
        total_biaya = halaman * harga_per_lembar

        print("\n" + "="*55)
        print(f"  TRANSAKSI -- {self.nama}")
        print("-"*55)
        print(f"  File       : {dokumen.nama_file}")
        print(f"  Halaman    : {halaman} x Rp{harga_per_lembar:,.0f} = Rp{total_biaya:,.0f}")
        print(f"  Saldo      : Rp{self.__saldo:,.0f}")
        print(f"  Kertas     : {mesin.get_stok_kertas()} lembar | Tinta: {mesin.get_stok_tinta()} unit")
        print("-"*55)

        if not mesin.stok_cukup_untuk(halaman):
            kertas_kurang = mesin.get_stok_kertas() < halaman
            tinta_kurang  = mesin.get_stok_tinta()  < halaman
            if kertas_kurang and tinta_kurang:
                print(f"  GAGAL: Stok kertas ({mesin.get_stok_kertas()}) DAN "
                      f"tinta ({mesin.get_stok_tinta()}) tidak cukup untuk {halaman} halaman!")
            elif kertas_kurang:
                print(f"  GAGAL: Stok kertas tidak cukup! "
                      f"Butuh {halaman}, tersisa {mesin.get_stok_kertas()}.")
            else:
                print(f"  GAGAL: Stok tinta tidak cukup! "
                      f"Butuh {halaman}, tersisa {mesin.get_stok_tinta()}.")
            print("="*55)
            return 'stok_habis'

        if self.__saldo < total_biaya:
            kekurangan = total_biaya - self.__saldo
            print(f"  GAGAL: Saldo tidak cukup!")
            print(f"         Dibutuhkan : Rp{total_biaya:,.0f}")
            print(f"         Saldo Anda : Rp{self.__saldo:,.0f}")
            print(f"         Kurang     : Rp{kekurangan:,.0f}")
            print("="*55)
            return 'saldo_kurang'

        self.potong_saldo(total_biaya)
        mesin.kurangi_stok(halaman)
        print(f"  SUKSES: Dokumen dicetak!")
        print(f"  Saldo terpotong : Rp{total_biaya:,.0f}")
        print(f"  Saldo tersisa   : Rp{self.__saldo:,.0f}")
        print(f"  Sisa kertas     : {mesin.get_stok_kertas()} lembar")
        print(f"  Sisa tinta      : {mesin.get_stok_tinta()} unit")
        print("="*55)
        mesin.cek_peringatan()
        return 'sukses'

def input_int(prompt: str, minimum: int = 0) -> int:
    while True:
        try:
            val = int(input(prompt))
            if val < minimum:
                print(f"  Nilai minimal {minimum}, coba lagi.")
            else:
                return val
        except ValueError:
            print("  Input harus angka bulat.")

def input_float(prompt: str, minimum: float = 0) -> float:
    while True:
        try:
            val = float(input(prompt))
            if val < minimum:
                print(f"  Nilai minimal {minimum}, coba lagi.")
            else:
                return val
        except ValueError:
            print("  Input harus angka.")

def tampilkan_status(mesin: MesinPrint):
    print("\n" + "-"*55)
    print("  STATUS MESIN")
    print(mesin.status_bar())
    print("-"*55 + "\n")

def lakukan_restock(mesin: MesinPrint):
    print("  (isi 0 jika tidak ingin restock item tersebut)")
    tambah_kertas = input_int("  Tambah Kertas (lembar) : ", 0)
    tambah_tinta  = input_int("  Tambah Tinta  (unit)   : ", 0)
    
    if tambah_kertas == 0 and tambah_tinta == 0:
        print("  Tidak ada yang di-restock.")
        if mesin.stok_habis():
            print("  >>> GAGAL: Stok masih kosong! Mesin tidak dapat digunakan untuk print. <<<\n")
        else:
            print()
    else:
        mesin.restock(tambah_kertas, tambah_tinta)
        
    tampilkan_status(mesin)

def menu_setelah_transaksi(mesin: MesinPrint) -> str:
    while True:
        print("\n  1. Pelanggan berikutnya")
        print("  2. Restock kertas / tinta")
        print("  3. Lihat status mesin")
        print("  4. Keluar sistem")
        pilihan = input("\n  Pilih [1-4]: ").strip()
        if pilihan == "1":
            return 'lanjut'
        elif pilihan == "2":
            lakukan_restock(mesin)
            return 'lanjut'
        elif pilihan == "3":
            tampilkan_status(mesin)
        elif pilihan == "4":
            return 'keluar'
        else:
            print("  Pilihan tidak valid, coba lagi.")

def menu_stok_habis(mesin: MesinPrint) -> str:
    print("\n" + "!"*55)
    print("  STOK TIDAK CUKUP -- Harus restock sebelum lanjut!")
    print("!"*55)
    tampilkan_status(mesin)
    while True:
        print("  1. Restock sekarang")
        print("  2. Keluar sistem")
        pilihan = input("\n  Pilih [1/2]: ").strip()
        if pilihan == "1":
            lakukan_restock(mesin)
            if mesin.stok_habis():
                continue
            return 'lanjut'
        elif pilihan == "2":
            return 'keluar'
        else:
            print("  Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    HARGA_PER_LEMBAR = 500.0

    print("\n" + "#"*55)
    print("   ITK-PRINT -- Sistem Layanan Fotokopi Mandiri")
    print("#"*55)

    print("\nSetup Mesin (sekali di awal)")
    print("-"*30)
    id_mesin    = input("  ID Mesin         : ")
    stok_kertas = input_int("  Stok Kertas awal : ", 0)
    stok_tinta  = input_int("  Stok Tinta awal  : ", 0)

    mesin = MesinPrint(id_mesin, stok_kertas, stok_tinta)
    tampilkan_status(mesin)

    while True:

        if mesin.stok_habis():
            aksi = menu_stok_habis(mesin)
            if aksi == 'keluar':
                break
            continue

        print("\nData Pelanggan Baru")
        print("-"*30)
        nama  = input("  Nama Pelanggan : ")
        saldo = input_float("  Saldo (Rp)     : ", 0)
        pelanggan = Pelanggan(nama, saldo)

        print("\nData Dokumen")
        print("-"*30)
        file = input("  Nama File      : ")
        hal  = input_int("  Jumlah Halaman : ", 1)
        dokumen = Dokumen(file, hal)

        hasil = pelanggan.cetak_dokumen(dokumen, mesin, HARGA_PER_LEMBAR)

        if hasil in ('sukses', 'saldo_kurang'):
            aksi = menu_setelah_transaksi(mesin)
            if aksi == 'keluar':
                break

        elif hasil == 'stok_habis':
            aksi = menu_stok_habis(mesin)
            if aksi == 'keluar':
                break

    print(f"\n  Sistem ditutup.")
    print(f"  Total halaman tercetak : {mesin.get_total_cetak()} halaman")
    print("  Terima kasih!\n")