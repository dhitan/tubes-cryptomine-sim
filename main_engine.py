import requests

class CryptoAsset:
    def __init__(self, nama, simbol, algoritma, total_network_hash, block_reward, block_time, harga=0.0):
        self.nama = nama
        self.simbol = simbol
        self.algoritma = algoritma
        self.total_network_hash = total_network_hash
        self.block_reward = block_reward
        self.block_time = block_time
        self.harga = harga # harga koin dalam rupiah
        


class MiningEngine:
    def __init__(self):
        self.maksimal = 100
        self.koleksi_koin = [None] * self.maksimal
        self.jumlah_koin = 0
        self.get_data_coingecko()

    def get_data_coingecko(self):
        # hardcode list coin pow (tnh, reward, waktu)
        daftar_koin = [
            {"id": "bitcoin", "n": "Bitcoin", "s": "BTC", "a": "SHA-256", "hash": 600e18, "rew": 3.125, "wkt": 600},
            {"id": "dogecoin", "n": "Dogecoin", "s": "DOGE", "a": "Scrypt", "hash": 1e15, "rew": 10000, "wkt": 60},
            {"id": "litecoin", "n": "Litecoin", "s": "LTC", "a": "Scrypt", "hash": 1e15, "rew": 6.25, "wkt": 150},
            {"id": "monero", "n": "Monero", "s": "XMR", "a": "RandomX", "hash": 2.5e9, "rew": 0.6, "wkt": 120},
            {"id": "ethereum-classic", "n": "Ethereum Classic", "s": "ETC", "a": "Etchash", "hash": 150e12, "rew": 2.56, "wkt": 13},
            {"id": "ravencoin", "n": "Ravencoin", "s": "RVN", "a": "KawPow", "hash": 6e12, "rew": 2500, "wkt": 60}
        ]
        
        # ambil harga real dari coingecko
        ids = ",".join([k["id"] for k in daftar_koin])
        u = "https://api.coingecko.com/api/v3/simple/price"
        p = {"ids": ids, "vs_currencies": "idr"}
        h = {'User-Agent': 'Mozilla/5.0'}
        
        harga_koin = {}
        try:
            res = requests.get(u, params=p, headers=h)
            harga_koin = res.json()
        except Exception as e:
            print("gagal ambil harga dari coingecko, memakai harga default")
            
        self.jumlah_koin = 0
        for k_data in daftar_koin:
            # cari harga di response json, kalau tidak ada set default 1000
            harga_idr = 1000
            if k_data["id"] in harga_koin and "idr" in harga_koin[k_data["id"]]:
                harga_idr = harga_koin[k_data["id"]]["idr"]
                
            k_baru = CryptoAsset(k_data["n"], k_data["s"], k_data["a"], k_data["hash"], k_data["rew"], k_data["wkt"], harga_idr)
            if self.jumlah_koin < self.maksimal:
                self.koleksi_koin[self.jumlah_koin] = k_baru
                self.jumlah_koin = self.jumlah_koin + 1

    def add_coin(self, koin_baru):
        if self.jumlah_koin < self.maksimal:
            self.koleksi_koin[self.jumlah_koin] = koin_baru
            self.jumlah_koin = self.jumlah_koin + 1

    def update_coin(self, koin_lama, koin_baru):
        i = 0
        ketemu = False
        while i < self.jumlah_koin and ketemu == False:
            if self.koleksi_koin[i] == koin_lama:
                self.koleksi_koin[i] = koin_baru
                ketemu = True
            i = i + 1

    def delete_coin(self, target):
        i = 0
        ketemu = False
        while i < self.jumlah_koin and ketemu == False:
            if self.koleksi_koin[i] == target:
                ketemu = True
                j = i
                while j < self.jumlah_koin - 1:
                    self.koleksi_koin[j] = self.koleksi_koin[j + 1]
                    j = j + 1
                self.koleksi_koin[self.jumlah_koin - 1] = None
                self.jumlah_koin = self.jumlah_koin - 1
            i = i + 1


    def cari_sequential(self, target):
        wadah = [None] * self.maksimal
        dapat = 0
        i = 0
        while i < self.jumlah_koin:
            k = self.koleksi_koin[i]
            if target.lower() in k.nama.lower():
                wadah[dapat] = k
                dapat = dapat + 1
            i = i + 1
        return wadah, dapat

    def cari_binary(self, target):
        kiri = 0
        kanan = self.jumlah_koin - 1
        ketemu = False
        hasil = None
        
        while kiri <= kanan and ketemu == False:
            tengah = (kiri + kanan) // 2
            k = self.koleksi_koin[tengah]
            
            if k.nama.lower() == target.lower():
                hasil = k
                ketemu = True
            elif k.nama.lower() < target.lower():
                kiri = tengah + 1
            else:
                kanan = tengah - 1
                
        return hasil

    def urutkan_selection(self, d, a):
        byk = self.jumlah_koin
        i = 0
        while i < byk - 1:
            plh = i
            j = i + 1
            while j < byk:
                k1 = self.koleksi_koin[plh]
                k2 = self.koleksi_koin[j]
                
                n1 = k1.total_network_hash
                n2 = k2.total_network_hash
                
                if d == 'block_reward':
                    n1 = k1.block_reward
                    n2 = k2.block_reward
                elif d == 'nama':
                    n1 = k1.nama.lower()
                    n2 = k2.nama.lower()
                    
                if a == 'Ascending':
                    if n2 < n1:
                        plh = j
                else:
                    if n2 > n1:
                        plh = j
                j = j + 1
                
            cad = self.koleksi_koin[i]
            self.koleksi_koin[i] = self.koleksi_koin[plh]
            self.koleksi_koin[plh] = cad
            i = i + 1

    def urutkan_insertion(self, d, a):
        byk = self.jumlah_koin
        i = 1
        while i < byk:
            k_kunci = self.koleksi_koin[i]
            
            n_kunci = k_kunci.block_reward
            if d == 'total_network_hash':
                n_kunci = k_kunci.total_network_hash
            elif d == 'nama':
                n_kunci = k_kunci.nama.lower()
                
            j = i - 1
            geser = True
            
            while j >= 0 and geser:
                k_j = self.koleksi_koin[j]
                
                n_j = k_j.block_reward
                if d == 'total_network_hash':
                    n_j = k_j.total_network_hash
                elif d == 'nama':
                    n_j = k_j.nama.lower()
                    
                tukar = False
                if a == 'Ascending':
                    if n_j > n_kunci:
                        tukar = True
                else:
                    if n_j < n_kunci:
                        tukar = True
                        
                if tukar:
                    self.koleksi_koin[j + 1] = self.koleksi_koin[j]
                    j = j - 1
                else:
                    geser = False
                    
            self.koleksi_koin[j + 1] = k_kunci
            i = i + 1
    
    def hitung_roi(self, hm, hn, tb, r, hrg, w, kwh, hw, durasi):
        # Menghitung total waktu (detik) dari input durasi (jam)
        total_detik = 3600 * durasi
        
        # b = jumlah block yang berhasil didapat jaringan selama durasi tersebut
        b = total_detik / tb
        
        # kr = (hashrate kita / hashrate jaringan) * total block * reward per block
        # Ini adalah estimasi koin yang kita dapatkan
        kr = (hm / hn) * b * r
        
        # k = pendapatan kotor (koin dikali harga per koin dalam kurs)
        k = kr * hrg
        
        # e = konsumsi energi dalam kWh (watt * jam dibagi 1000)
        e = (w * durasi) / 1000
        
        # l = total biaya listrik (konsumsi energi kWh dikali tarif dasar listrik)
        l = e * kwh
        
        # u = profit bersih (pendapatan kotor dikurangi biaya listrik)
        u = k - l
        
        # bm = break even point (kapan modal alat balik)
        if u <= 0:
            bm = 999999
            print("rugi bandar")
        else:
            bm = hw / u
            print("cuan")
            
        return b, kr, k, e, l, u, bm