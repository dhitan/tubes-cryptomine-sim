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
        pass

    def urutkan_selection(self, berdasarkan='difficulty'):
        pass

    def urutkan_insertion(self, berdasarkan='reward'):
        pass