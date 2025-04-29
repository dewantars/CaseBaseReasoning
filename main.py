import pandas as pd

# Fungsi keanggotaan segitiga
def keanggotaan_segitiga(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

# Proses Fuzzifikasi untuk Pelayanan
def fuzzifikasi_pelayanan(nilai):
    # Kategori keanggotaan untuk pelayanan
    buruk = keanggotaan_segitiga(nilai, 0, 0, 50)
    sedang = keanggotaan_segitiga(nilai, 30, 50, 70)
    baik = keanggotaan_segitiga(nilai, 50, 100, 100)
    return {"buruk": buruk, "sedang": sedang, "baik": baik}

# Proses Fuzzifikasi untuk harga
def fuzzifikasi_harga(nilai):
    # Kategori keanggotaan untuk harga
    murah = keanggotaan_segitiga(nilai, 25000, 25000, 40000)
    sedang = keanggotaan_segitiga(nilai, 30000, 40000, 50000)
    mahal = keanggotaan_segitiga(nilai, 40000, 55000, 55000)
    return {"murah": murah, "sedang": sedang, "mahal": mahal}

# Proses Inferensi Fuzzy
def inferensi_fuzzy(pelayanan_fuzzy, harga_fuzzy):
    # Aturan fuzzy
    aturan1 = min(pelayanan_fuzzy["baik"], harga_fuzzy["murah"])  # Layak tinggi
    aturan2 = min(pelayanan_fuzzy["sedang"], harga_fuzzy["sedang"])  # Layak sedang
    aturan3 = min(pelayanan_fuzzy["buruk"], harga_fuzzy["mahal"])  # Layak rendah
    return {"tinggi": aturan1, "sedang": aturan2, "rendah": aturan3}

# Proses Defuzzifikasi menggunakan Centroid
def defuzzifikasi(output_fuzzy):
    pembilang = (
        output_fuzzy["rendah"] * 25 +
        output_fuzzy["sedang"] * 50 +
        output_fuzzy["tinggi"] * 75
    )
    penyebut = (
        output_fuzzy["rendah"] +
        output_fuzzy["sedang"] +
        output_fuzzy["tinggi"]
    )
    return pembilang / penyebut if penyebut != 0 else 0

# Membaca data dari file Excel
def baca_excel(file_path):
    data = pd.read_excel(file_path)
    return data

# Menyimpan output ke file Excel
def simpan_ke_excel(file_path, data):
    data.to_excel(file_path, index=False)

# Program utama
if __name__ == "__main__":
    # Membaca data restoran
    file_input = 'restoran.xlsx'
    file_output = 'peringkat.xlsx'
    data = baca_excel(file_input)

    # Proses fuzzy untuk setiap restoran
    skor = []
    for _, baris in data.iterrows():
        pelayanan_fuzzy = fuzzifikasi_pelayanan(baris['Pelayanan'])
        harga_fuzzy = fuzzifikasi_harga(baris['harga'])
        output_fuzzy = inferensi_fuzzy(pelayanan_fuzzy, harga_fuzzy)
        nilai_skor = defuzzifikasi(output_fuzzy)
        skor.append(nilai_skor)

    # Tambahkan skor ke DataFrame
    data['Skor'] = skor

    # Pilih 5 restoran terbaik
    lima_terbaik = data.nlargest(5, 'Skor')

    # Simpan ke file output
    simpan_ke_excel(file_output, lima_terbaik)

    print(f"Peringkat 5 restoran terbaik berhasil disimpan ke file {file_output}.")