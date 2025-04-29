import pandas as pd

# Fungsi keanggotaan segitiga
def triangular_membership(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

# Proses Fuzzification untuk Pelayanan
def fuzzify_service(value):
    # Kategori keanggotaan untuk pelayanan
    poor = triangular_membership(value, 0, 0, 50)
    average = triangular_membership(value, 30, 50, 70)
    good = triangular_membership(value, 50, 100, 100)
    return {"poor": poor, "average": average, "good": good}

# Proses Fuzzification untuk harga
def fuzzify_price(value):
    # Kategori keanggotaan untuk harga
    cheap = triangular_membership(value, 25000, 25000, 40000)
    moderate = triangular_membership(value, 30000, 40000, 50000)
    expensive = triangular_membership(value, 40000, 55000, 55000)
    return {"cheap": cheap, "moderate": moderate, "expensive": expensive}

# Proses Inferensi Fuzzy
def fuzzy_inference(service_fuzzy, price_fuzzy):
    # Aturan fuzzy
    rule1 = min(service_fuzzy["good"], price_fuzzy["cheap"])  # Layak tinggi
    rule2 = min(service_fuzzy["average"], price_fuzzy["moderate"])  # Layak sedang
    rule3 = min(service_fuzzy["poor"], price_fuzzy["expensive"])  # Layak rendah
    return {"high": rule1, "medium": rule2, "low": rule3}

# Proses Defuzzification menggunakan Centroid
def defuzzify(output_fuzzy):
    numerator = (
        output_fuzzy["low"] * 25 +
        output_fuzzy["medium"] * 50 +
        output_fuzzy["high"] * 75
    )
    denominator = (
        output_fuzzy["low"] +
        output_fuzzy["medium"] +
        output_fuzzy["high"]
    )
    return numerator / denominator if denominator != 0 else 0

# Membaca data dari file Excel
# Komentar: Proses ini menggunakan pandas untuk membaca file xlsx
def read_excel(file_path):
    data = pd.read_excel(file_path)
    return data

# Menyimpan output ke file Excel
# Komentar: Fungsi ini menyimpan data ke file peringkat.xlsx
def save_to_excel(file_path, data):
    data.to_excel(file_path, index=False)

# Main program
if __name__ == "__main__":
    # Membaca data restoran
    input_file = 'restoran.xlsx'
    output_file = 'peringkat.xlsx'
    data = read_excel(input_file)

    # Proses fuzzy untuk setiap restoran
    scores = []
    for _, row in data.iterrows():
        service_fuzzy = fuzzify_service(row['Pelayanan'])
        price_fuzzy = fuzzify_price(row['harga'])
        output_fuzzy = fuzzy_inference(service_fuzzy, price_fuzzy)
        score = defuzzify(output_fuzzy)
        scores.append(score)

    # Tambahkan skor ke DataFrame
    data['Score'] = scores

    # Pilih 5 restoran terbaik
    top_5 = data.nlargest(5, 'Score')

    # Simpan ke file output
    save_to_excel(output_file, top_5)

    print(f"Peringkat 5 restoran terbaik berhasil disimpan ke file {output_file}.")