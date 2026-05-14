import requests

# class buat nyimpen data per koin nya
class CryptoAsset:
    def __init__(self, nama, simbol, algoritma, difficulty, reward):
        self.nama = nama
        self.simbol = simbol
        self.algoritma = algoritma
        self.difficulty = difficulty
        self.reward = reward

# Class ini buat nyimpen semua logic
class MiningEngine:
    def __init__(self):
        # Ini array buat nyimpen daftar koin yang udah di pull
        self.koleksi_koin = []

    # function buat get data dari CoinGecko
    def get_data_coingecko(self):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10, # Kita get 10 koin top aja dulu ya buat testing
            "page": 1
        }
        
        # Header biar gak dianggep bot sama CoinGecko
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            
            # Cek biar ga crash kalau API return message error
            if type(data) is list:
                # angka difficulty sama reward aku simulasiin dulu pake market rank sama harga.
                for item in data:
                    koin_baru = CryptoAsset(
                        nama=item['name'],
                        simbol=item['symbol'].upper(),
                        algoritma="SHA-256", # Dummy dulu, aslinya tiap koin beda
                        difficulty=item['market_cap_rank'] * 5000, 
                        reward=item['current_price'] * 0.05 
                    )
                    self.koleksi_koin.append(koin_baru)
            else:
                print("Kena limit/blokir dari API CoinGecko nih:", data)
                
        except Exception as e:
            print("Waduh, gagal get data API nih ngab:", e)

    # function buat tab kalkulasi mining.
    def hitung_estimasi_mining(self, koin, hashrate_user):
        estimasi_waktu = koin.difficulty / (hashrate_user + 1)
        daya_watt = hashrate_user * 1.5 
        return estimasi_waktu, daya_watt

    # function sequential search. ngescan array dari awal sampe dapet.
    def cari_sequential(self, nama_target):
        for koin in self.koleksi_koin:
            if koin.nama.lower() == nama_target.lower():
                return koin # Kalo ketemu, balikin object koinnya
        return None

    # BAGIAN BAWAH INI MASIH KOSONG, NTAR KU LANJUT
    def cari_binary(self, nama_target):
        pass

    def urutkan_selection(self, berdasarkan='difficulty'):
        pass

    def urutkan_insertion(self, berdasarkan='reward'):
        pass



# SCRIPT BUAT TESTING 

engine = MiningEngine()

print("Lagi get data dari CoinGecko, Sek Yaa...")
engine.get_data_coingecko()

# tampilin semua koin yang berhasil dipull 
print(f"\nBerhasil get {len(engine.koleksi_koin)} koin top:")
for koin in engine.koleksi_koin:
    print(f"- {koin.nama} ({koin.simbol}) | Diff: {koin.difficulty} | Reward: ${koin.reward:.2f}")

# script buat testing sequential search
target_koin = "Bitcoin"
print(f"\nCoba nyari koin: {target_koin}...")
hasil_cari = engine.cari_sequential(target_koin)

if hasil_cari:
    print(f"Ketemu nih! Simbolnya {hasil_cari.simbol}.")
    
    # sekalian ngetes fungsi kalkulasinya jalan atau ngga
    hashrate_ku = 1000 # misal hashrate usernya 1000
    waktu, daya = engine.hitung_estimasi_mining(hasil_cari, hashrate_ku)
    
    print(f"Estimasi waktu nambang: {waktu:.4f}")
    print(f"Daya yang kepake: {daya} Watt")
else:
    print("Wah, koinnya ga dapet di array.")