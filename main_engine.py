import requests

class CryptoAsset:
    def __init__(self, nama, simbol, algoritma, difficulty, reward, block_time, power_consumption):
        self.nama = nama
        self.simbol = simbol
        self.algoritma = algoritma
        self.difficulty = difficulty
        self.reward = reward
        self.block_time = block_time
        self.power_consumption = power_consumption

class MiningEngine:
    def __init__(self):
        self.koleksi_koin = []

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
                while i < banyak_data:
                    item = data[i]
                    nama_koin = item['name']
                    simbol_koin = item['symbol'].upper()
                    algo = "SHA-256"
                    diff = item['market_cap_rank'] * 5000
                    rew = item['current_price'] * 0.05
                    wkt_blok = 600 
                    dy_watt = 3500  
                    
                    koin_baru = CryptoAsset(nama_koin, simbol_koin, algo, diff, rew, wkt_blok, dy_watt)
                    self.koleksi_koin.append(koin_baru)
                    i = i + 1
            else:
                print("Kena limit/blokir dari API CoinGecko nih: " + str(data))
                
        except Exception as e:
            print("Waduh, gagal get data API nih ngab: " + str(e))

    def hitung_estimasi_mining(self, koin, hashrate_user):
        estimasi_waktu = koin.difficulty / (hashrate_user + 1)
        daya_watt = hashrate_user * 1.5 
        return estimasi_waktu, daya_watt

    def cari_sequential(self, nama_target):
        jumlah_koin = len(self.koleksi_koin)
        i = 0
        while i < jumlah_koin:
            koin_sekarang = self.koleksi_koin[i]
            if koin_sekarang.nama.lower() == nama_target.lower():
                return koin_sekarang
            i = i + 1
        return None

    def cari_binary(self, nama_target):
        kiri = 0
        kanan = len(self.koleksi_koin) - 1
        
        while kiri <= kanan:
            tengah = (kiri + kanan) // 2
            koin_tengah = self.koleksi_koin[tengah]
            
            if koin_tengah.nama.lower() == nama_target.lower():
                return koin_tengah
            
            if koin_tengah.nama.lower() < nama_target.lower():
                kiri = tengah + 1
            else:
                kanan = tengah - 1
                
        return None

    def urutkan_selection(self, berdasarkan='difficulty'):
        jumlah = len(self.koleksi_koin)
        i = 0
        while i < jumlah - 1:
            indeks_minimum = i
            j = i + 1
            while j < jumlah:
                koin_min = self.koleksi_koin[indeks_minimum]
                koin_j = self.koleksi_koin[j]
                
                nilai_min = koin_min.difficulty
                nilai_j = koin_j.difficulty
                
                if berdasarkan == 'reward':
                    nilai_min = koin_min.reward
                    nilai_j = koin_j.reward
                    
                if nilai_j < nilai_min:
                    indeks_minimum = j
                j = j + 1
                
            temp = self.koleksi_koin[i]
            self.koleksi_koin[i] = self.koleksi_koin[indeks_minimum]
            self.koleksi_koin[indeks_minimum] = temp
            i = i + 1

    def urutkan_insertion(self, berdasarkan='reward'):
        jumlah = len(self.koleksi_koin)
        i = 1
        while i < jumlah:
            koin_kunci = self.koleksi_koin[i]
            
            nilai_kunci = koin_kunci.reward
            if berdasarkan == 'difficulty':
                nilai_kunci = koin_kunci.difficulty
                
            j = i - 1
            sedang_geser = True
            
            while j >= 0 and sedang_geser:
                koin_j = self.koleksi_koin[j]
                
                nilai_j = koin_j.reward
                if berdasarkan == 'difficulty':
                    nilai_j = koin_j.difficulty
                    
                if nilai_j > nilai_kunci:
                    self.koleksi_koin[j + 1] = self.koleksi_koin[j]
                    j = j - 1
                else:
                    sedang_geser = False
                    
            self.koleksi_koin[j + 1] = koin_kunci
            i = i + 1