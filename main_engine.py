import requests

class CryptoAsset:
    def __init__(self, nama, simbol, algoritma, total_network_hash, reward, block_time):
        self.nama = nama
        self.simbol = simbol
        self.algoritma = algoritma
        self.total_network_hash = total_network_hash
        self.reward = reward
        self.block_time = block_time

class MiningEngine:
    def __init__(self):
        self.maksimal_koin = 100
        self.koleksi_koin = [None] * self.maksimal_koin
        self.jumlah_koin = 0

    def get_data_coingecko(self):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            if type(data) == list:
                i = 0
                banyak_data = len(data)
                self.jumlah_koin = 0
                while i < banyak_data:
                    item = data[i]
                    nama_koin = item['name']
                    simbol_koin = item['symbol'].upper()
                    algo = "SHA-256"
                    total_network_hash = item['market_cap_rank'] * 5000
                    rew = item['current_price'] * 0.05
                    wkt_blok = 600
                    
                    koin_baru = CryptoAsset(nama_koin, simbol_koin, algo, total_network_hash, rew, wkt_blok)
                    if self.jumlah_koin < self.maksimal_koin:
                        self.koleksi_koin[self.jumlah_koin] = koin_baru
                        self.jumlah_koin = self.jumlah_koin + 1
                    i = i + 1
            else:
                print("Kena limit dari API: " + str(data))
        except Exception as e:
            print("Gagal get data API: " + str(e))

    def hapus_data_koin(self, koin_target):
        i = 0
        ketemu = False
        while i < self.jumlah_koin and ketemu == False:
            if self.koleksi_koin[i] == koin_target:
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

    def cari_sequential(self, nama_target):
        i = 0
        ketemu = False
        hasil_pencarian = None
        while i < self.jumlah_koin and ketemu == False:
            koin_sekarang = self.koleksi_koin[i]
            if koin_sekarang.nama.lower() == nama_target.lower():
                hasil_pencarian = koin_sekarang
                ketemu = True
            i = i + 1
        return hasil_pencarian

    def cari_binary(self, nama_target):
        kiri = 0
        kanan = self.jumlah_koin - 1
        ketemu = False
        hasil_pencarian = None
        while kiri <= kanan and ketemu == False:
            tengah = (kiri + kanan) // 2
            koin_tengah = self.koleksi_koin[tengah]
            if koin_tengah.nama.lower() == nama_target.lower():
                hasil_pencarian = koin_tengah
                ketemu = True
            else:
                if koin_tengah.nama.lower() < nama_target.lower():
                    kiri = tengah + 1
                else:
                    kanan = tengah - 1
        return hasil_pencarian

    def urutkan_selection(self, berdasarkan='total_network_hash', urutan='Smallest'):
        i = 0
        while i < self.jumlah_koin - 1:
            indeks_terpilih = i
            j = i + 1
            while j < self.jumlah_koin:
                koin_pilih = self.koleksi_koin[indeks_terpilih]
                koin_j = self.koleksi_koin[j]
                
                nilai_pilih = koin_pilih.total_network_hash
                nilai_j = koin_j.total_network_hash
                
                if berdasarkan == 'reward':
                    nilai_pilih = koin_pilih.reward
                    nilai_j = koin_j.reward
                elif berdasarkan == 'nama':
                    nilai_pilih = koin_pilih.nama.lower()
                    nilai_j = koin_j.nama.lower()
                
                if urutan == 'Smallest':
                    if nilai_j < nilai_pilih:
                        indeks_terpilih = j
                else:
                    if nilai_j > nilai_pilih:
                        indeks_terpilih = j
                j = j + 1
            temp = self.koleksi_koin[i]
            self.koleksi_koin[i] = self.koleksi_koin[indeks_terpilih]
            self.koleksi_koin[indeks_terpilih] = temp
            i = i + 1

    def urutkan_insertion(self, berdasarkan='reward', urutan='Smallest'):
        i = 1
        while i < self.jumlah_koin:
            koin_kunci = self.koleksi_koin[i]
            nilai_kunci = koin_kunci.reward
            if berdasarkan == 'total_network_hash':
                nilai_kunci = koin_kunci.total_network_hash
            elif berdasarkan == 'nama':
                nilai_kunci = koin_kunci.nama.lower()
                
            j = i - 1
            sedang_geser = True
            while j >= 0 and sedang_geser == True:
                koin_j = self.koleksi_koin[j]
                nilai_j = koin_j.reward
                if berdasarkan == 'total_network_hash':
                    nilai_j = koin_j.total_network_hash
                elif berdasarkan == 'nama':
                    nilai_j = koin_j.nama.lower()
                
                harus_geser = False
                if urutan == 'Smallest':
                    if nilai_j > nilai_kunci:
                        harus_geser = True
                else:
                    if nilai_j < nilai_kunci:
                        harus_geser = True
                        
                if harus_geser == True:
                    self.koleksi_koin[j + 1] = self.koleksi_koin[j]
                    j = j - 1
                else:
                    sedang_geser = False
            self.koleksi_koin[j + 1] = koin_kunci
            i = i + 1