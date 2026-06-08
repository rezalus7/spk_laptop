# SPK Laptop — Metode SMART

Sistem Pendukung Keputusan pemilihan laptop menggunakan metode SMART.

## Struktur File

```
spk_laptop/
├── Beranda.py          ← Entry point (Login & Register)
├── state.py            ← Data, session state, kalkulasi SMART
├── theme.py            ← CSS global (inject ke semua halaman)
├── requirements.txt
├── .streamlit/
│   └── config.toml     ← Konfigurasi tema & server
└── pages/
    ├── 1_Dashboard.py  ← Analisis & rekomendasi SMART
    ├── 2_Data_Laptop.py← CRUD data laptop
    └── 3_Riwayat.py    ← Riwayat pencarian
```

## Cara Jalankan Lokal

```bash
pip install streamlit
cd spk_laptop
streamlit run Beranda.py
```

## Deploy ke Streamlit Cloud

1. Upload folder ini ke **GitHub repository** (public atau private)
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Klik **New app**
4. Pilih repo → branch → set **Main file path** = `Beranda.py`
5. Klik **Deploy**

## Akun Demo

| Username   | Password | Role       |
|------------|----------|------------|
| admin      | 123      | Admin      |
| mahasiswa  | 123      | Mahasiswa  |

## Fitur

- **Login & Register** — halaman terpisah, form stabil
- **Dashboard SMART** — filter kriteria, komputasi utilitas, ranking
- **Data Laptop** — tabel lengkap + CRUD (khusus admin)
- **Riwayat** — log semua analisis; admin lihat semua, mahasiswa lihat milik sendiri
