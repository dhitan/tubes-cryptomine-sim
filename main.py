import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
from ui_main import Ui_Form
from main_engine import MiningEngine, CryptoAsset



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
        self.tata_letak.addRow("hash:", self.i_hash)
        self.tata_letak.addRow("algo:", self.i_algo)
        self.tata_letak.addRow("hadiah:", self.i_hadiah)
        self.tata_letak.addRow("waktu:", self.i_waktu)
        
        self.tombol = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.tombol.accepted.connect(self.accept)
        self.tombol.rejected.connect(self.reject)
        
        self.tata_letak.addRow(self.tombol)
        
    def get_data(self):
        return {
            'nama': self.i_nama.text(),
            'simbol': self.i_simbol.text(),
            'total_network_hash': self.i_hash.text(),
            'algoritma': self.i_algo.text(),
            'block_reward': self.i_hadiah.text(),
            'block_time': self.i_waktu.text()
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
        
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem("Total Network Hash")
        self.ui.comboBox.addItem("Block Reward")
        self.ui.comboBox.addItem("Nama")
        
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItem("Ascending")
        self.ui.comboBox_2.addItem("Descending")
        
        self.engine = MiningEngine()
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels([
            "Nama", "Simbol", "Total Network Hash", "Algoritma", "Block Reward", "Block Time(det)", "Aksi"
        ])
        self.render_tableWidget()
        self.ui.lineEdit.textChanged.connect(self.search)
        self.ui.pushButton_4.clicked.connect(self.addCoin)
        self.ui.comboBox.currentTextChanged.connect(self.main_sort)
        self.ui.comboBox_2.currentTextChanged.connect(self.main_sort)
        
        self.ui.pushButton.clicked.connect(self.show_about)
        self.ui.pushButton_6.clicked.connect(self.ekspor_data)
        self.ui.pushButton_2.clicked.connect(self.gas_hitung)

    def show_about(self):
        QMessageBox.information(self, "About", "Aplikasi Simulasi Mining Crypto\nTugas Besar Alpro")

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

    def addCoin(self):
        layar = CoinFormDialog(self)
        if layar.exec():
            isi = layar.get_data()
            k_baru = CryptoAsset(isi['nama'], isi['simbol'], isi['algoritma'], float(isi['total_network_hash']), float(isi['block_reward']), float(isi['block_time']))
            self.engine.add_coin(k_baru)
            self.render_tableWidget()

    def editCoin(self, target):
        layar = CoinFormDialog(self, target)
        if layar.exec():
            isi = layar.get_data()
            k_baru = CryptoAsset(isi['nama'], isi['simbol'], isi['algoritma'], float(isi['total_network_hash']), float(isi['block_reward']), float(isi['block_time']))
            self.engine.update_coin(target, k_baru)
            self.render_tableWidget()

    def delCoin(self, target):
        tanya = QMessageBox.question(self, 'awas', "yakin mau buang " + str(target.nama) + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if tanya == QMessageBox.Yes:
            self.engine.delete_coin(target)
            self.render_tableWidget()

    def search(self, teks):
        if teks == "":
            self.render_tableWidget()
        else:
            kumpulan, banyak = self.engine.cari_sequential(teks)
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

    def show_chart(self):
        import matplotlib.pyplot as plt
        nama_koin = []
        harga_koin = []
        i = 0
        while i < len(self.engine.koleksi_koin):
            nama_koin.append(self.engine.koleksi_koin[i].simbol)
            harga_koin.append(self.engine.koleksi_koin[i].block_reward)
            i = i + 1
            
        plt.bar(nama_koin, harga_koin)
        plt.show()
    
    def ekspor_data(self):
        self.engine.bikin_csv()
        QMessageBox.information(self, "mantap", "laporan udah jadi csv")

    def gas_hitung(self):
        n_mentah = self.ui.comboBox_3.currentText()
        n = n_mentah.split(" ")[0]
        
        h = float(self.ui.lineEdit_2.text())
        t = float(self.ui.lineEdit_4.text())
        
        k = self.engine.cari_sequential(n)
        
        if k != None:
            b, kr, p, l, u, bm = self.engine.hitung_roi(h, k.total_network_hash, k.block_time, k.block_reward, 15000, 120, t, 15000000)
            
            self.ui.label_63.setText(str(b))
            self.ui.label_65.setText(str(kr))
            self.ui.label_69.setText(str(l))
            self.ui.label_72.setText(str(p))
            self.ui.label_74.setText(str(u))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Kishar()
    window.show()
    sys.exit(app.exec())