import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
from ui_main import Ui_Form
from main_engine import MiningEngine

class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem("Total Network Hash")
        self.ui.comboBox.addItem("Block Reward")
        self.ui.comboBox.addItem("Nama")
        
        self.engine = MiningEngine()
        self.engine.get_data_coingecko()
        self.render_tableWidget()

        self.ui.lineEdit.textChanged.connect(self.fitur_cari)
        self.ui.comboBox.currentTextChanged.connect(self.jalankan_pengurutan)
        self.ui.comboBox_2.currentTextChanged.connect(self.jalankan_pengurutan)
        self.ui.pushButton.clicked.connect(self.tampilkan_grafik)

    def render_tableWidget(self):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Nama", "Simbol", "Total Network Hash", "Algoritma", "Block Reward", "Block Time(det)", "Aksi"])
        
        baris = 0
        i = 0
        while i < self.engine.jumlah_koin:
            koin = self.engine.koleksi_koin[i]
            self.ui.tableWidget.insertRow(baris)
            
            item1 = QTableWidgetItem(str(koin.nama))
            self.ui.tableWidget.setItem(baris, 0, item1)
            
            item2 = QTableWidgetItem(str(koin.simbol))
            self.ui.tableWidget.setItem(baris, 1, item2)
            
            item3 = QTableWidgetItem(str(koin.total_network_hash))
            self.ui.tableWidget.setItem(baris, 2, item3)
            
            item4 = QTableWidgetItem(str(koin.algoritma))
            self.ui.tableWidget.setItem(baris, 3, item4)
            
            item5 = QTableWidgetItem(str(koin.reward))
            self.ui.tableWidget.setItem(baris, 4, item5)
            
            item6 = QTableWidgetItem(str(koin.block_time))
            self.ui.tableWidget.setItem(baris, 5, item6)
            
            self.buat_tombol_aksi_tabel(baris, koin)
            baris = baris + 1
            i = i + 1

    def buat_tombol_aksi_tabel(self, baris, koin):
        widget_aksi = QWidget()
        layout_aksi = QHBoxLayout(widget_aksi)
        
        layout_aksi.setContentsMargins(4, 4, 4, 4)
        layout_aksi.setSpacing(5)

        btn_edit = QPushButton("Edit")
        btn_hapus = QPushButton("Hapus")

        btn_hapus.setStyleSheet("color: red;")

        layout_aksi.addWidget(btn_edit)
        layout_aksi.addWidget(btn_hapus)

        btn_edit.clicked.connect(lambda checked, k=koin: self.edit_koin(k))
        btn_hapus.clicked.connect(lambda checked, k=koin: self.hapus_koin(k))

        kolom_aksi = 6
        self.ui.tableWidget.setCellWidget(baris, kolom_aksi, widget_aksi)

    def edit_koin(self, koin):
        print("Tombol edit dipencet untuk koin: " + str(koin.nama))

    def hapus_koin(self, koin):
        kotak_pesan = QMessageBox()
        kotak_pesan.setWindowTitle("Konfirmasi Hapus")
        kotak_pesan.setText("Apakah kamu yakin ingin menghapus koin " + str(koin.nama) + "?")
        kotak_pesan.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        pilihan = kotak_pesan.exec()
        
        if pilihan == QMessageBox.Yes:
            self.engine.hapus_data_koin(koin)
            self.render_tableWidget()

    def fitur_cari(self, teks):
        if teks == "":
            self.render_tableWidget()
        else:
            hasil = self.engine.cari_sequential(teks)
            self.ui.tableWidget.setRowCount(0)
            if hasil != None:
                self.ui.tableWidget.insertRow(0)
                item1 = QTableWidgetItem(str(hasil.nama))
                self.ui.tableWidget.setItem(0, 0, item1)
                item2 = QTableWidgetItem(str(hasil.simbol))
                self.ui.tableWidget.setItem(0, 1, item2)
                item3 = QTableWidgetItem(str(hasil.total_network_hash))
                self.ui.tableWidget.setItem(0, 2, item3)
                item4 = QTableWidgetItem(str(hasil.algoritma))
                self.ui.tableWidget.setItem(0, 3, item4)
                item5 = QTableWidgetItem(str(hasil.reward))
                self.ui.tableWidget.setItem(0, 4, item5)
                item6 = QTableWidgetItem(str(hasil.block_time))
                self.ui.tableWidget.setItem(0, 5, item6)

    def jalankan_pengurutan(self, teks_apapun):
        kategori = self.ui.comboBox.currentText()
        arah = self.ui.comboBox_2.currentText()
        
        if kategori == "Total Network Hash":
            self.engine.urutkan_selection("total_network_hash", arah)
        elif kategori == "Block Reward":
            self.engine.urutkan_insertion("reward", arah)
        elif kategori == "Nama":
            self.engine.urutkan_selection("nama", arah)
            
        self.render_tableWidget()
        self.tampilkan_grafik()

    def tampilkan_grafik(self):
        import matplotlib.pyplot as plt
        nama_koin = []
        harga_koin = []
        i = 0
        while i < self.engine.jumlah_koin:
            nama_koin.append(self.engine.koleksi_koin[i].simbol)
            harga_koin.append(self.engine.koleksi_koin[i].reward)
            i = i + 1
            
        plt.bar(nama_koin, harga_koin)
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec())