
import pandas as pd
import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from multiprocessing import freeze_support

base_dir = Path(__file__).resolve().parent
data_path = base_dir / "data" / "hour.csv"
output_dir = base_dir / "outputs"


# Fungsi pengolahan satu bagian data
def proses_bagian(bagian):
    hasil = {}

    for bulan, jumlah in zip(
        bagian["mnth"], bagian["cnt"]
    ):
        hasil[bulan] = hasil.get(bulan, 0) + jumlah

    return hasil


# Menggabungkan hasil dari setiap proses
def gabungkan(hasil_bagian):
    hasil = {}

    for bagian in hasil_bagian:
        for bulan, jumlah in bagian.items():
            hasil[bulan] = hasil.get(bulan, 0) + jumlah

    return hasil


# Pengolahan serial: menggunakan satu proses
def serial(data):
    return proses_bagian(data)


# Pengolahan paralel: membagi data ke beberapa proses
def paralel(data, jumlah_proses=2):
    potongan = [
        data.iloc[i::jumlah_proses]
        for i in range(jumlah_proses)
    ]

    with ProcessPoolExecutor(
        max_workers=jumlah_proses
    ) as executor:
        hasil_bagian = list(
            executor.map(proses_bagian, potongan)
        )

    return gabungkan(hasil_bagian)


# Fungsi utama eksperimen
def main():
    # Membaca dataset
    df = pd.read_csv(data_path)

    # Menyiapkan data numerik
    df = df[["mnth", "cnt"]].dropna().copy()
    df["mnth"] = df["mnth"].astype(int)
    df["cnt"] = df["cnt"].astype(int)

    # Menyiapkan folder output
    output_dir.mkdir(exist_ok=True)

    catatan = []

    # Eksperimen pada beberapa ukuran data
    for pengali in [1, 5, 10, 20]:

        # Pengulangan data untuk simulasi beban.
        # Baris tambahan bukan observasi baru yang nyata.
        data_uji = pd.concat(
            [df] * pengali,
            ignore_index=True
        )

        # Pengukuran waktu serial
        mulai = time.perf_counter()
        hasil_serial = serial(data_uji)
        waktu_serial = time.perf_counter() - mulai

        # Pengukuran waktu paralel
        mulai = time.perf_counter()
        hasil_paralel = paralel(data_uji, 2)
        waktu_paralel = time.perf_counter() - mulai

        # Memastikan hasil kedua metode sama
        sama = hasil_serial == hasil_paralel

        # Menghitung speedup
        speedup = (
            waktu_serial / waktu_paralel
            if waktu_paralel > 0 else None
        )

        catatan.append({
            "baris": len(data_uji),
            "serial_detik": waktu_serial,
            "paralel_detik": waktu_paralel,
            "speedup": speedup,
            "hasil_sama": sama
        })

    # Menyimpan hasil benchmark ke CSV
    hasil = pd.DataFrame(catatan)
    hasil.to_csv(
        output_dir / "benchmark.csv",
        index=False
    )

    print("\n=== HASIL BENCHMARK ===")
    print(hasil.round(4).to_string(index=False))

    # Membuat grafik perbandingan
    ax = hasil.plot(
        x="baris",
        y=["serial_detik", "paralel_detik"],
        marker="o"
    )

    ax.set_xlabel("Jumlah baris data")
    ax.set_ylabel("Waktu (detik)")
    ax.set_title("Benchmark Serial vs Paralel")

    plt.tight_layout()
    plt.savefig(
        output_dir / "benchmark.png",
        dpi=150
    )
    plt.close()

    print(f"\nHasil CSV: {output_dir / 'benchmark.csv'}")
    print(f"Grafik: {output_dir / 'benchmark.png'}")


# Pengaman wajib untuk multiprocessing di Windows
if __name__ == "__main__":
    freeze_support()
    main()
