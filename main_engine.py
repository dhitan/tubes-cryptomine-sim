import requests
import json
import os



class CryptoAsset:
    def __init__(self, nama, simbol, algoritma, total_network_hash, block_reward, block_time):
        self.nama = nama
        self.simbol = simbol
        self.algoritma = algoritma
        self.total_network_hash = total_network_hash
        self.block_reward = block_reward
        self.block_time = block_time
        

    def to_dict(self):
        return {
            'nama': self.nama,
            'simbol': self.simbol,
            'algoritma': self.algoritma,
            'total_network_hash': self.total_network_hash,
            'block_reward': self.block_reward,
            'block_time': self.block_time
        }

# serialization
    @classmethod
    def from_dict(cls, data):
        return cls(
            nama=data.get('nama', ''),
            simbol=data.get('simbol', ''),
            algoritma=data.get('algoritma', ''),
            total_network_hash=data.get('total_network_hash', 0),
            block_reward=data.get('block_reward', 0),
            block_time=data.get('block_time', 0)
        )

class MiningEngine:
    def __init__(self):
        self.maksimal = 100
        self.koleksi_koin = [None] * self.maksimal
        self.jumlah_koin = 0
        self.get_data_coingecko()

    def get_data_coingecko(self):
        u = "https://api.coingecko.com/api/v3/coins/markets"
        p = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
        h = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            res = requests.get(u, params=p, headers=h)
            d = res.json()
            
            if type(d) == list:
                i = 0
                byk = len(d)
                self.jumlah_koin = 0
                while i < byk:
                    brg = d[i]
                    n = brg['name']
                    s = brg['symbol'].upper()
                    a = "SHA-256"
                    hash_val = brg['market_cap_rank'] * 5000
                    rew = brg['current_price'] * 0.05
                    wkt = 600
                    
                    k_baru = CryptoAsset(n, s, a, hash_val, rew, wkt)
                    if self.jumlah_koin < self.maksimal:
                        self.koleksi_koin[self.jumlah_koin] = k_baru
                        self.jumlah_koin = self.jumlah_koin + 1
                    i = i + 1
            else:
                print("kena limit")
        except Exception as e:
            print("gagal ambil data")

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

    def hitung_estimasi_mining(self, koin, hashrate_user):
        estimasi_waktu = koin.total_network_hash / (hashrate_user + 1)
        daya_watt = hashrate_user * 1.5 
        return estimasi_waktu, daya_watt

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
        byk = len(self.koleksi_koin)
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
        byk = len(self.koleksi_koin)
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
    
    def hitung_roi(self, hm, hn, tb, r, hrg, w, kwh, hw):
        b = 86400 / tb
        kr = (hm / hn) * b * r
        k = kr * hrg
        l = ((w * 24) / 1000) * kwh
        u = k - l
        
        if u <= 0:
            bm = 999999
            print("rugi bandar")
        else:
            bm = hw / u
            print("cuan")
            
        return b, kr, k, l, u, bm

    def bikin_csv(self):
        f = open("laporan.csv", "w")
        f.write("koin,simbol,hash,algo,hadiah,waktu\n")
        
        i = 0
        banyak = len(self.koleksi_koin)
        while i < banyak:
            k = self.koleksi_koin[i]
            t = str(k.nama) + "," + str(k.simbol) + "," + str(k.total_network_hash) + "," + str(k.algoritma) + "," + str(k.block_reward) + "," + str(k.block_time) + "\n"
            f.write(t)
            i = i + 1
            
        f.close()
        print("beres cetak")