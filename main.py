import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout
from ui_main import Ui_Form
from main_engine import MiningEngine 

class Kishar(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.engine = MiningEngine()
        self.engine.get_data_coingecko()
        self.render_tableWidget()

        self.ui.lineEdit.textChanged.connect(self.search)
        self.ui.comboBox.currentTextChanged.connect(self.main_sort)
        
        self.ui.pushButton.clicked.connect(self.show_chart)

    def render_tableWidget(self):
        self.ui.tableWidget.setRowCount(0)
        
        baris = 0
        for koin in self.engine.koleksi_koin:
            self.ui.tableWidget.insertRow(baris)
            
            item1 = QTableWidgetItem(str(koin.nama))
            self.ui.tableWidget.setItem(baris, 0, item1)
            
            item2 = QTableWidgetItem(str(koin.simbol))
            self.ui.tableWidget.setItem(baris, 1, item2)
            
            item3 = QTableWidgetItem(str(koin.difficulty))
            self.ui.tableWidget.setItem(baris, 2, item3)
            
            item4 = QTableWidgetItem(str(koin.algoritma))
            self.ui.tableWidget.setItem(baris, 3, item4)
            
            item5 = QTableWidgetItem(str(koin.reward))
            self.ui.tableWidget.setItem(baris, 4, item5)
            
            item6 = QTableWidgetItem(str(koin.block_time))
            self.ui.tableWidget.setItem(baris, 5, item6)
            
            item7 = QTableWidgetItem(str(koin.power_consumption))
            self.ui.tableWidget.setItem(baris, 6, item7)
            
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

        kolom_aksi = 7 
        self.ui.tableWidget.setCellWidget(baris, kolom_aksi, widget_aksi)

    def editCoin(self, koin):
        print("Edit",koin.nama,"triggred")

    def delCoin(self, koin):
        print("Delete",koin.nama,"triggred")
        if koin in self.engine.koleksi_koin:
            self.engine.koleksi_koin.remove(koin) 
            self.render_tableWidget()

    def search(self, teks):
        if teks == "":
            self.engine.koleksi_koin.clear()
            self.engine.get_data_coingecko()
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
                item3 = QTableWidgetItem(str(hasil.difficulty))
                self.ui.tableWidget.setItem(0, 2, item3)
                item4 = QTableWidgetItem(str(hasil.algoritma))
                self.ui.tableWidget.setItem(0, 3, item4)
                item5 = QTableWidgetItem(str(hasil.reward))
                self.ui.tableWidget.setItem(0, 4, item5)
                item6 = QTableWidgetItem(str(hasil.block_time))
                self.ui.tableWidget.setItem(0, 5, item6)
                item7 = QTableWidgetItem(str(hasil.power_consumption))
                self.ui.tableWidget.setItem(0, 6, item7)

    def main_sort(self, teks):
        if teks == "Difficulty":
            self.engine.urutkan_selection("difficulty")
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