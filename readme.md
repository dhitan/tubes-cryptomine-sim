# Selamat datang semua
Kami menggunakan qt creator untuk membuat design UI<br>
Aplikasi ini dibuat menggunakan pyside6 hasil konversi dari Qt. <br>
Bilamana ada salah dari kalian yang ingin melihat file raw .ui silahkan kunjungi main.ui di root folder project ini lalu jalankan perintah ini di terminal:
(ganti ui_main.py ke nama yang kalian inginkan, dan pastikan anda berada di root directory)

>pip install pyside6

>pyside6-uic main.ui -o ui_main.py

Maka akan muncul file baru bernama ui_main.py(atau nama lain yang kalian inginkan) yang berisi kode python hasil konversi dari main.ui<br>
Untuk menjalankan aplikasi ini gunakan perintah

>py main.py

logika di balik project ini berada di main_engine.py<br>
notepad rumus yang kami gunakan untuk mencari ROI berada di file notepad.ipynb

Program ini menggunakan coingecko api untuk mengambil data realtime(delay 2 menit).<br>
Hasil export to csv berada di file laporan_mining.csv(root folder)

berikut dokumentasi, dan referensi yang kami gunakan untuk membuat project ini:
- https://www.geeksforgeeks.org/python-how-to-access-coingecko-api/
- https://doc.qt.io/qtforpython-6/examples/index.html
- https://doc.qt.io/qtforpython-6/overviews/qtwidgets-gallery.html
- https://doc.qt.io/qtforpython-6/tools/pyside-designer.html#pyside6-designer

- https://www.cryptocompare.com/mining/calculator/btc
- https://www.nicehash.com/profitability-calculator

bagaimana roi dihitung? silahkan kunjungi notepad.ipynb

terima kasih.