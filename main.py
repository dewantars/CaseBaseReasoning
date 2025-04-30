import pandas as pd

# Fungsi keanggotaan segitiga
def keanggotaan_segitiga(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a) if (b - a) != 0 else 1
    elif b < x < c:
        return (c - x) / (c - b) if (c - b) != 0 else 1

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

# Proses Inferensi Fuzzy dengan model Mamdani
def inferensi_fuzzy(pelayanan_fuzzy, harga_fuzzy):
    aturan = {
        "rendah": [],
        "sedang": [],
        "tinggi": []
    }

    # Kombinasi aturan:
    # Baik
    aturan["tinggi"].append(min(pelayanan_fuzzy["baik"], harga_fuzzy["murah"]))
    aturan["tinggi"].append(min(pelayanan_fuzzy["baik"], harga_fuzzy["sedang"]))
    aturan["sedang"].append(min(pelayanan_fuzzy["baik"], harga_fuzzy["mahal"]))

    # Sedang
    aturan["tinggi"].append(min(pelayanan_fuzzy["sedang"], harga_fuzzy["murah"]))
    aturan["sedang"].append(min(pelayanan_fuzzy["sedang"], harga_fuzzy["sedang"]))
    aturan["rendah"].append(min(pelayanan_fuzzy["sedang"], harga_fuzzy["mahal"]))

    # Buruk
    aturan["sedang"].append(min(pelayanan_fuzzy["buruk"], harga_fuzzy["murah"]))
    aturan["rendah"].append(min(pelayanan_fuzzy["buruk"], harga_fuzzy["sedang"]))
    aturan["rendah"].append(min(pelayanan_fuzzy["buruk"], harga_fuzzy["mahal"]))

    return {
        "tinggi": max(aturan["tinggi"]),
        "sedang": max(aturan["sedang"]),
        "rendah": max(aturan["rendah"])
    }


# Proses Agregasi Fuzzy
def agregasi_fuzzy(output_fuzzy):
    # Fungsi keanggotaan keluaran
    domain = range(0, 101)  # Asumsikan domain keluaran adalah 0-100
    tinggi = [min(output_fuzzy["tinggi"], keanggotaan_segitiga(x, 70, 100, 100)) for x in domain]
    sedang = [min(output_fuzzy["sedang"], keanggotaan_segitiga(x, 20, 50, 80)) for x in domain]
    rendah = [min(output_fuzzy["rendah"], keanggotaan_segitiga(x, 0, 25, 30)) for x in domain]

    # Agregasi dengan maximum
    hasil_agregasi = [max(rendah[i], sedang[i], tinggi[i]) for i in range(len(domain))]
    return domain, hasil_agregasi

# Proses Defuzzifikasi menggunakan Centroid
def defuzzifikasi_mamdani(domain, hasil_agregasi):
    pembilang = sum(domain[i] * hasil_agregasi[i] for i in range(len(domain)))
    penyebut = sum(hasil_agregasi)
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
        domain, hasil_agregasi = agregasi_fuzzy(output_fuzzy)
        nilai_skor = defuzzifikasi_mamdani(domain, hasil_agregasi)
        # Tampilkan hasil ke konsol
        print(f"\nID Pelanggan: {baris['id Pelanggan']}")
        print(f"Pelayanan: {baris['Pelayanan']}, Harga: {baris['harga']}")
        print("Fuzzifikasi Pelayanan:", pelayanan_fuzzy)
        print("Fuzzifikasi Harga:", harga_fuzzy)
        print("Inferensi Fuzzy:", output_fuzzy)
        print("Skor Defuzzifikasi:", nilai_skor)
        skor.append(nilai_skor)

    # Tambahkan skor ke DataFrame
    data['Skor'] = skor

    # Pilih 5 restoran terbaik
    lima_terbaik = data.nlargest(5, 'Skor')

    # Simpan ke file output
    simpan_ke_excel(file_output, lima_terbaik)

    print(f"Peringkat 5 restoran terbaik berhasil disimpan ke file {file_output}.")
