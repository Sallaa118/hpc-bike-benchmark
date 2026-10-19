# HPC Bike Sharing Benchmark: Serial vs Parallel Processing

## 📌 Deskripsi Proyek

Proyek ini merupakan eksperimen sederhana **High-Performance Computing (HPC)** untuk membandingkan performa pemrosesan data secara serial dan paralel menggunakan Python.

Dataset yang digunakan adalah Bike Sharing Dataset dari UCI Machine Learning Repository. Eksperimen dilakukan dengan mengagregasi jumlah penyewaan sepeda berdasarkan bulan, kemudian membandingkan waktu eksekusi metode serial dan paralel menggunakan dua proses.

Ukuran data diperbesar dengan mengulang dataset sebanyak 1, 5, 10, dan 20 kali untuk menyimulasikan peningkatan beban pemrosesan.

Proyek ini bertujuan memahami bahwa pemrosesan paralel tidak selalu lebih cepat daripada pemrosesan serial, terutama ketika pekerjaan yang dilakukan cukup sederhana dan biaya koordinasi proses relatif besar.

## 🎯 Tujuan

1. Memahami perbedaan pemrosesan serial dan paralel.
2. Mengimplementasikan parallel processing menggunakan `ProcessPoolExecutor`.
3. Mengukur waktu eksekusi pada beberapa ukuran data.
4. Memastikan hasil pemrosesan serial dan paralel tetap konsisten.
5. Menghitung speedup sebagai ukuran perbandingan performa.
6. Menganalisis pengaruh ukuran data dan overhead multiprocessing terhadap waktu eksekusi.

## 📂 Struktur Proyek

```text
hpc-bike-benchmark/
├── data/
│   └── hour.csv
├── outputs/
│   ├── benchmark.csv
│   └── benchmark.png
├── benchmark.py
├── requirements.txt
├── README.md
└── .gitignore
```

Keterangan:

- `data/hour.csv`: dataset penyewaan sepeda.
- `benchmark.py`: kode utama eksperimen.
- `outputs/benchmark.csv`: hasil pengukuran waktu.
- `outputs/benchmark.png`: grafik perbandingan waktu eksekusi.
- `requirements.txt`: daftar library Python yang dibutuhkan.
- `.gitignore`: daftar file dan folder yang tidak perlu diunggah ke GitHub.

Folder `outputs/` dibuat otomatis oleh program ketika eksperimen dijalankan.

## 📊 Dataset

Dataset yang digunakan adalah **Bike Sharing Dataset**, yang disediakan oleh UCI Machine Learning Repository.

Sumber: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset

File yang digunakan adalah `hour.csv`, yang berisi catatan penyewaan sepeda per jam beserta variabel waktu, kondisi cuaca, dan jumlah penyewaan.

Dalam eksperimen ini, hanya dua kolom yang digunakan:

| Kolom | Keterangan |
|---|---|
| `mnth` | Bulan, dengan nilai 1–12 |
| `cnt` | Jumlah penyewaan sepeda pada observasi tersebut |

Dataset asli memiliki 17.379 baris. Data kemudian diperbanyak secara artifisial untuk menguji perubahan waktu eksekusi pada beban yang lebih besar.

**Catatan:** baris hasil pengulangan bukan observasi penyewaan baru yang nyata. Pengulangan hanya digunakan sebagai simulasi beban komputasi.

## 🛠️ Teknologi yang Digunakan

- **Python 3** — bahasa pemrograman.
- **Pandas** — membaca dan memproses dataset.
- **Matplotlib** — membuat grafik benchmark.
- **Concurrent Futures** — menjalankan proses paralel melalui `ProcessPoolExecutor`.
- **Time** — mengukur waktu eksekusi.
- **Pathlib** — membuat folder keluaran.

## ⚙️ Cara Menjalankan Proyek

### 1. Clone repository

```bash
git clone <URL_REPOSITORY>
cd hpc-bike-benchmark
```

Ganti `<URL_REPOSITORY>` dengan URL repository GitHub milikmu.

### 2. Buat virtual environment

```bash
python -m venv .venv
```

Aktifkan di Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instal library

Jalankan:

```bash
pip install -r requirements.txt
```

Jika `requirements.txt` belum tersedia, gunakan:

```bash
pip install pandas matplotlib
```

### 4. Siapkan dataset

Unduh Bike Sharing Dataset dari sumber UCI di atas. Ekstrak dataset, lalu letakkan `hour.csv` di folder `data/`.

Pastikan struktur folder sesuai dengan kode:

```text
hpc-bike-benchmark/
└── data/
    └── hour.csv
```

### 5. Jalankan benchmark

Dari folder utama proyek, jalankan:

```bash
python benchmark.py
```

Program akan membandingkan waktu pemrosesan serial dan paralel, memeriksa kesamaan hasil, menghitung speedup, menyimpan tabel hasil ke CSV, dan menghasilkan grafik.

## 🔬 Metodologi Eksperimen

### 1. Persiapan data

Dataset dibaca menggunakan Pandas. Kolom `mnth` dan `cnt` dipilih, baris dengan nilai kosong di kedua kolom tersebut dihapus, lalu kedua kolom dikonversi menjadi tipe integer.

### 2. Pemrosesan serial

Seluruh data diproses menggunakan satu proses. Program menjumlahkan nilai `cnt` untuk setiap bulan.

### 3. Pemrosesan paralel

Data dibagi menjadi dua bagian, kemudian masing-masing bagian diproses oleh proses terpisah menggunakan `ProcessPoolExecutor`.

Hasil dari kedua proses digabungkan untuk memperoleh total penyewaan per bulan.

### 4. Pengujian ukuran data

| Pengali | Jumlah baris |
|---:|---:|
| 1× | 17.379 |
| 5× | 86.895 |
| 10× | 173.790 |
| 20× | 347.580 |

### 5. Evaluasi

Pengukuran dilakukan menggunakan `time.perf_counter()`.

Speedup dihitung dengan rumus:

**Speedup = waktu serial / waktu paralel**

Jika speedup lebih besar dari 1, paralel lebih cepat. Jika lebih kecil dari 1, serial lebih cepat.

Program juga membandingkan hasil agregasi kedua metode untuk memastikan hasilnya sama.

## 📈 Hasil Eksperimen

Hasil berikut diperoleh dari eksekusi program pada lingkungan pengujian yang digunakan.

| Baris data | Serial (detik) | Paralel (detik) | Speedup | Hasil sama |
|---:|---:|---:|---:|:---:|
| 17.379 | 0,0027 | 1,3154 | 0,0021 | Ya |
| 86.895 | 0,0249 | 1,3423 | 0,0185 | Ya |
| 173.790 | 0,0322 | 1,2403 | 0,0260 | Ya |
| 347.580 | 0,0582 | 1,2234 | 0,0475 | Ya |

### Temuan utama

**1. Metode serial lebih cepat pada seluruh pengujian.**

Waktu serial berkisar antara 0,0027 dan 0,0582 detik, sedangkan metode paralel membutuhkan sekitar 1,22–1,34 detik.

**2. Hasil perhitungan kedua metode konsisten.**

Nilai `hasil_sama` adalah `True` pada seluruh pengujian. Artinya, agregasi jumlah penyewaan per bulan yang dihasilkan metode serial dan paralel identik.

**3. Tidak ditemukan speedup pada konfigurasi ini.**

Seluruh nilai speedup berada di bawah 1. Pada pengujian 347.580 baris, metode serial sekitar 21 kali lebih cepat berdasarkan pengukuran yang diperoleh.

**4. Penambahan ukuran data belum membuat metode paralel lebih unggul.**

Meskipun data diperbanyak hingga 20 kali, biaya pembagian data, pembuatan proses, komunikasi antarpemrosesan, dan penggabungan hasil masih mendominasi waktu metode paralel.

## 🧠 Analisis dan Kesimpulan

Eksperimen menunjukkan bahwa parallel processing tidak otomatis meningkatkan performa. Keuntungan pemrosesan paralel bergantung pada karakteristik pekerjaan, ukuran beban, biaya komunikasi, dan overhead pembuatan proses.

Dalam proyek ini, operasi agregasi per bulan cukup sederhana sehingga metode serial dapat menyelesaikannya dengan sangat cepat. Sebaliknya, metode paralel membutuhkan waktu tambahan untuk menyiapkan proses dan mengirimkan bagian data.

Dengan demikian, **metode serial merupakan pilihan yang lebih efisien untuk beban dan implementasi yang diuji**.

Namun, hasil ini tidak membuktikan bahwa pemrosesan paralel selalu lebih lambat. Eksperimen lanjutan dapat menggunakan komputasi yang lebih intensif, mengulang setiap pengukuran beberapa kali, serta membandingkan median waktu untuk memperoleh evaluasi performa yang lebih kuat.

## 🚀 Pengembangan Selanjutnya

- Mengulang setiap pengujian beberapa kali dan menggunakan median waktu.
- Menggunakan operasi komputasi yang lebih intensif agar perbandingan HPC lebih representatif.
- Membandingkan penggunaan 2, 4, dan lebih banyak proses.
- Mengukur waktu persiapan proses secara terpisah dari waktu komputasi.
- Menguji dataset yang lebih besar tanpa hanya mengulang baris yang sama.
- Membandingkan penggunaan multiprocessing dengan pendekatan vektorisasi Pandas atau NumPy.

## ⚠️ Keterbatasan

1. Data tambahan merupakan pengulangan dataset, bukan observasi baru.
2. Operasi agregasi yang digunakan relatif sederhana.
3. Pengukuran waktu dapat dipengaruhi aktivitas sistem dan overhead proses.
4. Eksperimen menggunakan dua proses paralel, sehingga hasilnya tidak mewakili semua konfigurasi perangkat keras.
5. Hasil pengukuran berlaku untuk lingkungan pengujian saat ini dan tidak otomatis berlaku pada komputer lain.

---

**Kategori:** High-Performance Computing (HPC)  
**Bahasa:** Python  
**Dataset:** UCI Bike Sharing Dataset  
**Metode:** Serial Processing vs Parallel Processing  
**Status:** Eksperimen awal selesai
