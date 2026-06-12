import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
from ui_main import Ui_Form
from main_engine import MiningEngine, CryptoAsset

class CoinFormDialog(QDialog):
    def __init__(self, parent=None, coin=None):
        super().__init__(parent)
        self.setWindowTitle("Form Aset Kripto")
        
        self.layout = QFormLayout(self)
        
        self.nama_input = QLineEdit(self)
        self.simbol_input = QLineEdit(self)
        self.hash_input = QLineEdit(self)
        self.algo_input = QLineEdit(self)
        self.reward_input = QLineEdit(self)
        self.time_input = QLineEdit(self)
        
        if coin:
            self.nama_input.setText(coin.nama)
            self.simbol_input.setText(coin.simbol)
            self.hash_input.setText(str(coin.total_network_hash))
            self.algo_input.setText(coin.algoritma)
            self.reward_input.setText(str(coin.reward))
            self.time_input.setText(str(coin.block_time))
            
        self.layout.addRow("Nama:", self.nama_input)
        self.layout.addRow("Simbol:", self.simbol_input)
        self.layout.addRow("Total Network Hash:", self.hash_input)
        self.layout.addRow("Algoritma:", self.algo_input)
        self.layout.addRow("Block Reward:", self.reward_input)
        self.layout.addRow("Block Time (detik):", self.time_input)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        self.layout.addRow(self.buttons)
        
    def get_data(self):
        return {
            'nama': self.nama_input.text(),
            'simbol': self.simbol_input.text(),
            'total_network_hash': self.hash_input.text(),
            'algoritma': self.algo_input.text(),
            'reward': self.reward_input.text(),
            'block_time': self.time_input.text()
        }

class Kishar(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.engine = MiningEngine()
        
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels([
            "Nama", "Simbol", "Total Network Hash", "Algoritma", "Block Reward", "Block Time(det)", "Aksi"
        ])
        
        self.render_tableWidget()

        self.ui.lineEdit.textChanged.connect(self.search)
        self.ui.pushButton_4.clicked.connect(self.addCoin)
        self.ui.comboBox.currentTextChanged.connect(self.main_sort)
        
        self.ui.pushButton.clicked.connect(self.show_chart)

    def render_tableWidget(self):
        self.ui.tableWidget.setRowCount(0)
        
        baris = 0
        
        for koin in self.engine.koleksi_koin:
            self.ui.tableWidget.insertRow(baris)
            
            atribut_koin = [
                koin.nama, koin.simbol, koin.total_network_hash, 
                koin.algoritma, koin.reward, koin.block_time
            ]
            
            for kolom, nilai in enumerate(atribut_koin):
                item = QTableWidgetItem(str(nilai))
                self.ui.tableWidget.setItem(baris, kolom, item)
            
            self.btn_table_action(baris, koin)
            baris = baris + 1

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
        dialog = CoinFormDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            koin_baru = CryptoAsset(data['nama'], data['simbol'], data['algoritma'], 
                                    float(data['total_network_hash']), float(data['reward']), float(data['block_time']))
            self.engine.add_coin(koin_baru)
            self.render_tableWidget()

    def editCoin(self, koin):
        dialog = CoinFormDialog(self, koin)
        if dialog.exec():
            data = dialog.get_data()
            koin_baru = CryptoAsset(data['nama'], data['simbol'], data['algoritma'], 
                                    float(data['total_network_hash']), float(data['reward']), float(data['block_time']))
            self.engine.update_coin(koin, koin_baru)
            self.render_tableWidget()

    def delCoin(self, koin):
        reply = QMessageBox.question(self, 'Konfirmasi Hapus', f"Apakah kamu yakin ingin menghapus {koin.nama}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.engine.delete_coin(koin)
            self.render_tableWidget()

    def search(self, teks):
        if teks == "":
            self.engine.koleksi_koin.clear()
            self.engine.load_data()
            self.render_tableWidget()
        else:
            hasil = self.engine.cari_sequential(teks)
            self.ui.tableWidget.setRowCount(0)
            if hasil != None:
                self.ui.tableWidget.insertRow(0)
                atribut_koin = [
                    hasil.nama, hasil.simbol, hasil.total_network_hash, 
                    hasil.algoritma, hasil.reward, hasil.block_time
                ]
                for kolom, nilai in enumerate(atribut_koin):
                    item = QTableWidgetItem(str(nilai))
                    self.ui.tableWidget.setItem(0, kolom, item)

    def main_sort(self, teks):
        if teks == "Difficulty":
            self.engine.urutkan_selection("total_network_hash")
        elif teks == "Block Reward":
            self.engine.urutkan_insertion("reward")
            
        self.render_tableWidget()
        self.show_chart()

    def show_chart(self):
        import matplotlib.pyplot as plt
        nama_koin = []
        harga_koin = []
        i = 0
        while i < len(self.engine.koleksi_koin):
            nama_koin.append(self.engine.koleksi_koin[i].simbol)
            harga_koin.append(self.engine.koleksi_koin[i].reward)
            i = i + 1
            
        plt.bar(nama_koin, harga_koin)
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Kishar()
    window.show()
    sys.exit(app.exec())