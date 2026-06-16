import sys
import csv
import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QAbstractItemView, QLabel, QComboBox
from ui_main import Ui_Form
from main_engine import MiningEngine, CryptoAsset

# fungsi pemisah satuan hash (k, m, g, t, p, e)
def parse_hash(teks):
    teks = str(teks).strip()
    parts = teks.split(" ")
    try:
        angka = float(parts[0])
    except:
        angka = 0.0
    
    if len(parts) > 1:
        s = parts[1].upper()
        if s == 'K': angka = angka * 1e3
        elif s == 'M': angka = angka * 1e6
        elif s == 'G': angka = angka * 1e9
        elif s == 'T': angka = angka * 1e12
        elif s == 'P': angka = angka * 1e15
        elif s == 'E': angka = angka * 1e18
    return angka



class CoinFormDialog(QDialog):
    def __init__(self, induk=None, koin=None):
        super().__init__(induk)
        self.setWindowTitle("form data kripto")
        self.tata_letak = QFormLayout(self)
        self.i_nama = QLineEdit(self)
        self.i_simbol = QLineEdit(self)
        self.i_hash = QLineEdit(self)
        self.i_algo = QLineEdit(self)
        self.i_hadiah = QLineEdit(self)
        self.i_waktu = QLineEdit(self)
        
        if koin:
            self.i_nama.setText(koin.nama)
            self.i_simbol.setText(koin.simbol)
            self.i_hash.setText(str(koin.total_network_hash))
            self.i_algo.setText(koin.algoritma)
            self.i_hadiah.setText(str(koin.block_reward))
            self.i_waktu.setText(str(koin.block_time))
            
        self.tata_letak.addRow("nama:", self.i_nama)
        self.tata_letak.addRow("simbol:", self.i_simbol)
        # instruksi tnh di form
        self.tata_letak.addRow("tnh (contoh: 500 T):", self.i_hash)
        self.tata_letak.addRow("algo:", self.i_algo)
        self.tata_letak.addRow("hadiah:", self.i_hadiah)
        self.tata_letak.addRow("waktu:", self.i_waktu)
        
        self.tombol = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.tombol.accepted.connect(self.accept)
        self.tombol.rejected.connect(self.reject)
        
        self.tata_letak.addRow(self.tombol)
        
    def get_data(self):
        tnh = parse_hash(self.i_hash.text())
        try:
            reward = float(self.i_hadiah.text())
            waktu = float(self.i_waktu.text())
        except:
            reward = 0.0
            waktu = 0.0
            
        if tnh < 0 or reward < 0 or waktu < 0:
            QMessageBox.warning(self, "Error", "Input tidak boleh bernilai negatif/minus!")
            
        return {
            'nama': self.i_nama.text(),
            'simbol': self.i_simbol.text(),
            # parsing tnh yang diinput pengguna
            'total_network_hash': max(0.0, tnh),
            'algoritma': self.i_algo.text(),
            'block_reward': max(0.0, reward),
            'block_time': max(0.0, waktu)
        }

class Kishar(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.tabWidget.setCurrentIndex(0)
        
        self.ui.frame_14.hide()
        self.ui.frame_15.hide()
        self.ui.frame_16.hide()
        self.ui.frame_2.hide()
        self.ui.frame_13.hide()
        self.ui.frame_21.hide()
        self.ui.label_24.hide() # Judul Perhitungan Sesi
        self.ui.label_25.hide() # Judul Param Input
        self.ui.label_62.hide() # Judul Sesi mining
        
        self.ui.label_64.setText("Total Block")
        
        self.ui.label_46.setText("Hashrate Pengguna (contoh: 500 M)")
        
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem("Total Network Hash")
        self.ui.comboBox.addItem("Block Reward")
        self.ui.comboBox.addItem("Nama")
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItem("Ascending")
        self.ui.comboBox_2.addItem("Descending")
        self.engine = MiningEngine()
        
        # membuat tabel menjadi readonly
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels([
            "Nama", "Simbol", "Total Network Hash", "Algoritma", "Block Reward", "Block Time(det)", "Aksi"
        ])
        
        # inisialisasi daftar sesi laporan
        self.daftar_sesi = []
        self.hasil_terakhir = None
        
        # tambah input daya hardware (watt) secara dinamis
        self.label_watt = QLabel("Daya Hardware (Watt)")
        self.input_watt = QLineEdit()
        
        idx = self.ui.verticalLayout_10.indexOf(self.ui.pushButton_2)
        self.ui.verticalLayout_10.insertWidget(idx, self.label_watt)
        self.ui.verticalLayout_10.insertWidget(idx + 1, self.input_watt)
        
        # koneksi tombol laporan
        self.ui.pushButton_3.clicked.connect(self.simpan_sesi)
        self.ui.pushButton_6.clicked.connect(self.export_csv)
        self.ui.pushButton_5.clicked.connect(self.hapus_semua_sesi)
        
        self.render_tableWidget()
        
        # dropdown sequental/binsearch
        self.combo_search = QComboBox()
        self.combo_search.addItems(["Sequential Search", "Binary Search"])
        self.ui.horizontalLayout.insertWidget(0, self.combo_search)
        
        self.update_combobox_aset()
        
        self.ui.lineEdit.textChanged.connect(self.search)
        self.combo_search.currentTextChanged.connect(lambda: self.search(self.ui.lineEdit.text()))
        self.ui.pushButton_4.clicked.connect(self.addCoin)
        self.ui.comboBox.currentTextChanged.connect(self.main_sort)
        self.ui.comboBox_2.currentTextChanged.connect(self.main_sort)
        
        self.ui.pushButton.clicked.connect(self.show_about)
        self.ui.pushButton_2.clicked.connect(self.gas_hitung)

    def show_about(self):
        QMessageBox.information(self, "About", "Aplikasi Simulasi Mining Crypto\nTugas Besar Alpro Telkom University Surabaya\n- Dhitan Hakim Arendrayuda 108102500027\n- Muhammad Ghufroon 108102530005")

    def render_tableWidget(self):
        self.ui.tableWidget.setRowCount(0)
        baris = 0
        i = 0
        
        while i < self.engine.jumlah_koin:
            koin = self.engine.koleksi_koin[i]
            self.ui.tableWidget.insertRow(baris)
            
            atribut = [
                koin.nama, koin.simbol, koin.total_network_hash, 
                koin.algoritma, koin.block_reward, koin.block_time
            ]
            
            kolom = 0
            while kolom < 6:
                item = QTableWidgetItem(str(atribut[kolom]))
                self.ui.tableWidget.setItem(baris, kolom, item)
                kolom = kolom + 1
            
            self.btn_table_action(baris, koin)
            baris = baris + 1
            i = i + 1

    def btn_table_action(self, baris, koin):
        widget_aksi = QWidget()
        layout_aksi = QHBoxLayout(widget_aksi)
        
        layout_aksi.setContentsMargins(4, 4, 4, 4) 
        layout_aksi.setSpacing(5)

        btn_edit = QPushButton("Edit")
        btn_hapus = QPushButton("Hapus")

        btn_hapus.setStyleSheet("color: red;")

        layout_aksi.addWidget(btn_edit)
        layout_aksi.addWidget(btn_hapus)

        btn_edit.clicked.connect(lambda checked, k=koin: self.editCoin(k))
        btn_hapus.clicked.connect(lambda checked, k=koin: self.delCoin(k))

        kolom_aksi = 6 
        self.ui.tableWidget.setCellWidget(baris, kolom_aksi, widget_aksi)

    def update_combobox_aset(self):
        self.ui.comboBox_3.clear()
        i = 0
        while i < self.engine.jumlah_koin:
            k = self.engine.koleksi_koin[i]
            self.ui.comboBox_3.addItem(f"{k.nama} ({k.simbol})")
            i = i + 1

    def addCoin(self):
        layar = CoinFormDialog(self)
        if layar.exec():
            isi = layar.get_data()
            k_baru = CryptoAsset(isi['nama'], isi['simbol'], isi['algoritma'], float(isi['total_network_hash']), float(isi['block_reward']), float(isi['block_time']))
            self.engine.add_coin(k_baru)
            self.render_tableWidget()
            self.update_combobox_aset()

    def editCoin(self, target):
        layar = CoinFormDialog(self, target)
        if layar.exec():
            isi = layar.get_data()
            k_baru = CryptoAsset(isi['nama'], isi['simbol'], isi['algoritma'], float(isi['total_network_hash']), float(isi['block_reward']), float(isi['block_time']))
            self.engine.update_coin(target, k_baru)
            self.render_tableWidget()
            self.update_combobox_aset()

    def delCoin(self, target):
        tanya = QMessageBox.question(self, 'awas', "yakin mau buang " + str(target.nama) + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if tanya == QMessageBox.Yes:
            self.engine.delete_coin(target)
            self.render_tableWidget()
            self.update_combobox_aset()

    def search(self, teks):
        if teks == "":
            self.render_tableWidget()
        else:
            mode = self.combo_search.currentText()
            
            if mode == "Sequential Search":
                kumpulan, banyak = self.engine.cari_sequential(teks)
            else:
                hasil = self.engine.cari_binary(teks)
                if hasil:
                    kumpulan = [hasil]
                    banyak = 1
                else:
                    kumpulan = []
                    banyak = 0
                    
            self.ui.tableWidget.setRowCount(0)
            baris = 0
            i = 0
            while i < banyak:
                k = kumpulan[i]
                self.ui.tableWidget.insertRow(baris)
                atribut = [
                    k.nama, k.simbol, k.total_network_hash, 
                    k.algoritma, k.block_reward, k.block_time
                ]
                kolom = 0
                while kolom < 6:
                    item = QTableWidgetItem(str(atribut[kolom]))
                    self.ui.tableWidget.setItem(baris, kolom, item)
                    kolom = kolom + 1
                self.btn_table_action(baris, k)
                baris = baris + 1
                i = i + 1

    def main_sort(self, buang_aja):
        kat = self.ui.comboBox.currentText()
        arh = self.ui.comboBox_2.currentText()

        if kat == "Total Network Hash":
            self.engine.urutkan_selection("total_network_hash", arh)
        elif kat == "Block Reward":
            self.engine.urutkan_insertion("block_reward", arh)
        elif kat == "Nama":
            self.engine.urutkan_selection("nama", arh)
            
        self.render_tableWidget()
    

    def gas_hitung(self):
        n_mentah = self.ui.comboBox_3.currentText()
        n = n_mentah.split(" ")[0] # mengambil nama koin dari combo box
        
        # mengambil input pengguna lalu dipisah dan divalidasi
        try:
            h_mentah = self.ui.lineEdit_2.text()
            h = parse_hash(h_mentah) # hashrate pengguna
            
            durasi = float(self.ui.lineEdit_3.text()) # durasi mining dalam jam
            t = float(self.ui.lineEdit_4.text()) # tarif listrik Rp/kWh
            w = float(self.input_watt.text()) # daya hardware watt
        except:
            QMessageBox.warning(self, "Error", "Input harus berupa angka valid!")
            return
            
        # cek angka minus
        if h < 0 or durasi < 0 or t < 0 or w < 0:
            QMessageBox.warning(self, "Error", "Input tidak boleh bernilai negatif/minus!")
            return
        
        # mencari aset yang dipilih
        kumpulan, banyak = self.engine.cari_sequential(n)
        
        if banyak > 0:
            k = kumpulan[0]
            # Kalkulasi ROI menggunakan k.harga asli dari coingecko
            b, kr, p, e, l, u = self.engine.hitung_roi(h, k.total_network_hash, k.block_time, k.block_reward, k.harga, w, t, 15000000, durasi)
            
            # Memasukkan hasil perhitungan ke label UI tanpa notasi ilmiah (scientific notation)
            self.ui.label_63.setText(f"{b:.2f}")            # total block yang didapat
            self.ui.label_65.setText(f"{kr:.8f}")           # estimasi reward (jumlah koin)
            self.ui.label_67.setText(f"{e:.2f}")            # konsumsi energi (kWh)
            self.ui.label_69.setText(f"{l:.2f}")            # total biaya listrik (Rp)
            self.ui.label_72.setText(f"{p:.2f}")            # pendapatan kotor (Rp)
            self.ui.label_74.setText(f"{u:.2f}")            # profit bersih (Rp)
            
            # simpan hasil terakhir untuk fitur simpan sesi
            self.hasil_terakhir = {
                "aset": k.nama,
                "simbol": k.simbol,
                "hashrate": h,
                "durasi": durasi,
                "reward": kr,
                "energi": e,
                "tarif": t,
                "total_biaya": l,
                "tanggal": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    def simpan_sesi(self):
        if self.hasil_terakhir is not None:
            self.daftar_sesi.append(self.hasil_terakhir)
            self.hasil_terakhir = None # agar tidak tersimpan dobel
            self.update_tabel_laporan()
            self.update_total_laporan()
            QMessageBox.information(self, "SUKSES", "SESI TERSIMPAN")
        else:
            QMessageBox.warning(self, "ERROR", "Anda belum melakukan kalkulasi")

    def update_tabel_laporan(self):
        self.ui.tableWidget_2.setRowCount(0)
        for baris, sesi in enumerate(self.daftar_sesi):
            self.ui.tableWidget_2.insertRow(baris)
            atribut = [
                sesi["aset"], sesi["simbol"], sesi["hashrate"], 
                sesi["durasi"], f"{sesi['reward']:.8f}", f"{sesi['energi']:.2f}", 
                sesi["tarif"], f"{sesi['total_biaya']:.2f}", sesi["tanggal"]
            ]
            for kolom, data in enumerate(atribut):
                item = QTableWidgetItem(str(data))
                self.ui.tableWidget_2.setItem(baris, kolom, item)

    def update_total_laporan(self):
        t_biaya = sum(s["total_biaya"] for s in self.daftar_sesi)
        t_reward = sum(s["reward"] for s in self.daftar_sesi)
        t_energi = sum(s["energi"] for s in self.daftar_sesi)
        t_sesi = len(self.daftar_sesi)
        
        self.ui.label_79.setText(f"Total biaya listrik: Rp {t_biaya:.2f}")
        self.ui.label_77.setText(f"Total reward: {t_reward:.8f}")
        self.ui.label_78.setText(f"Total energi: {t_energi:.2f} kWh")
        self.ui.label_80.setText(f"Total sesi: {t_sesi}")

    def export_csv(self):
        if not self.daftar_sesi:
            QMessageBox.warning(self, "error", "tidak ada data untuk diekspor!")
            return
            
        try:
            with open('laporan_mining.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["aset", "simbol", "hashrate", "durasi", "est_reward", "energi", "tarif_listrik", "total_biaya", "tanggal"])
                for s in self.daftar_sesi:
                    writer.writerow([s["aset"], s["simbol"], s["hashrate"], s["durasi"], s["reward"], s["energi"], s["tarif"], s["total_biaya"], s["tanggal"]])
            QMessageBox.information(self, "sukses", "data berhasil diekspor ke laporan_mining.csv")
        except Exception as e:
            QMessageBox.critical(self, "error", f"gagal mengekspor: {str(e)}")

    def hapus_semua_sesi(self):
        self.daftar_sesi.clear()
        self.update_tabel_laporan()
        self.update_total_laporan()
        QMessageBox.information(self, "sukses", "semua riwayat sesi berhasil dihapus")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Kishar()
    window.show()
    sys.exit(app.exec())