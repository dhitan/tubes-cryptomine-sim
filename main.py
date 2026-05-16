import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout
from ui_main import Ui_Form
from main_engine import MiningEngine 

class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.engine = MiningEngine()
        self.engine.get_data_coingecko()
        self.render_tableWidget()

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
            
            self.buat_tombol_aksi_tabel(baris, koin)
            baris = baris + 1

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

        kolom_aksi = 7 
        self.ui.tableWidget.setCellWidget(baris, kolom_aksi, widget_aksi)

    def edit_koin(self, koin):
        print("Tombol edit dipencet untuk koin: " + str(koin.nama))

    def hapus_koin(self, koin):
        print("Tombol hapus dipencet untuk koin: " + str(koin.nama))
        if koin in self.engine.koleksi_koin:
            self.engine.koleksi_koin.remove(koin) 
            self.render_tableWidget()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec())