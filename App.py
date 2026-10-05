import datetime
import math
import streamlit as st

st.set_page_config(
    page_title="Smart AI Cut & Fitness Planner", page_icon="💪", layout="wide"
)

st.title("🔥 Smart AI Cutting & Fitness Planner with Auto-Evaluation")
st.markdown(
    "Aplikasi web pintar dengan penyesuaian gender, AI food logging via foto,"
    " serta sistem evaluasi otomatis saat progres mandek."
)

with st.sidebar:
  st.header("📝 Profil & Data Fisik")
  user_name = st.text_input("Nama Pengguna", "Berryl")
  gender = st.selectbox("Jenis Kelamin", ["Pria", "Wanita"])
  current_weight = st.number_input("Berat Badan Sekarang (kg)", 30.0, 200.0, 75.0)
  current_height = st.number_input("Tinggi Badan (cm)", 100.0, 220.0, 168.0)
  age = st.number_input("Usia (tahun)", 15, 80, 25)

  st.divider()
  st.header("🎯 Target & Kondisi Tubuh")
  current_body_fat = st.slider("Lemak Badan Saat Ini (%)", 5.0, 40.0, 20.0, 0.5)

  # Rekomendasi batas aman target lemak berdasarkan gender
  min_target_fat = 8.0 if gender == "Pria" else 15.0
  target_body_fat = st.slider(
      "Target Lemak Badan (%)", min_target_fat, 35.0, 10.0, 0.5
  )

  activity_level = st.selectbox(
      "Level Aktivitas",
      [
          "Jarang Olahraga",
          "Olahraga Ringan",
          "Olahraga Sedang",
          "Angkat Beban Intensif (6x Seminggu)",
      ],
      index=3,
  )

# 1. Kalkulasi Berdasarkan Gender
current_fat_mass = current_weight * (current_body_fat / 100.0)
current_lbm = current_weight - current_fat_mass
target_weight = current_lbm / (1.0 - (target_body_fat / 100.0))
total_fat_to_lose = max(0.0, current_weight - target_weight)

# BMR Mifflin-St Jeor dengan penyesuaian gender
if gender == "Pria":
  bmr = (10 * current_weight) + (6.25 * current_height) - (5 * age) + 5
else:
  bmr = (10 * current_weight) + (6.25 * current_height) - (5 * age) - 161

multiplier = {
    "Jarang Olahraga": 1.2,
    "Olahraga Ringan": 1.375,
    "Olahraga Sedang": 1.55,
    "Angkat Beban Intensif (6x Seminggu)": 1.725,
}[activity_level]

tdee = bmr * multiplier
target_calories = max(1200, int(tdee - 500))

# Tampilan Layout Utama dengan Tab
tab1, tab2, tab3 = st.tabs(
    ["📊 Dashboard & Target", "📸 AI Food Scanner & Log", "🔍 Evaluasi & Progres"]
)

with tab1:
  st.subheader(f"Ringkasan Target Cutting ({gender})")
  c1, c2, c3 = st.columns(3)
  c1.metric("Target Berat Badan", f"{target_weight:.1f} kg", f"-{total_fat_to_lose:.1f} kg lemak")
  c2.metric("Kalori Harian", f"{target_calories} kkal", f"Defisit dari TDEE {int(tdee)}")
  c3.metric(
      "Protein Direkomendasikan",
      f"{int(current_weight * 2.2)} gram",
      "Jaga Massa Otot",
  )

  st.info(
      "💡 Catatan untuk Gender: Target lemak diatur dengan batas aman fisiologis"
      f" minimum {min_target_fat}% untuk kategori {gender.lower()}."
  )

with tab2:
  st.subheader("📸 Catat Makanan dengan AI Photo Scanner")
  st.markdown(
      "Upload foto makanan lo di sini. AI akan mendeteksi isi piring, jenis"
      " makanan, dan mengalkulasi kalorinya secara otomatis ke dalam total"
      " harian."
  )

  uploaded_file = st.file_uploader(
      "Pilih foto makanan...", type=["jpg", "jpeg", "png"]
  )
  if uploaded_file is not None:
    st.image(
        uploaded_file, caption="Foto Makanan Diunggah", use_container_width=True
    )
    if st.button("Analisis Foto & Hitung Kalori"):
      # Simulasi hasil pembacaan AI Vision
      st.success(
          "✅ **Makanan Terdeteksi:** Dada Ayam Bakar (150g) + Nasi Merah (100g)"
          " + Tumis Pakcoy."
      )
      st.markdown("""
            * **Estimasi Kalori:** 420 kkal
            * **Protein:** 38g | **Karbo:** 45g | **Lemak:** 8g
            * *Status:* Berhasil ditambahkan ke log harian!
            """)

with tab3:
  st.subheader("🔍 Smart Evaluation (Evaluasi Jika Mandek)")
  st.markdown(
      "Masukkan data berat badan terbaru setelah 2 minggu berjalan untuk"
      " mendeteksi apakah ada stagnasi (*plateau*)."
  )

  last_weight_check = st.number_input(
      "Berat Badan 2 Minggu Lalu (kg)", 30.0, 200.0, current_weight
  )
  current_weight_check = st.number_input(
      "Berat Badan Minggu Ini (kg)", 30.0, 200.0, current_weight
  )

  if st.button("Jalankan Evaluasi Otomatis"):
    weight_diff = current_weight_check - last_weight_check
    if weight_diff >= 0:
      st.error(
          "⚠️ **Terdeteksi Stagnasi / Kenaikan Berat Badan!**"
      )
      st.markdown("""
                **Kemungkinan Analisis & Solusi:**
                1. **Kalori Gelap:** Ada makanan/minuman manis atau minyak tersembunyi yang belum tercatat di foto scanner.
                2. **Adaptasi Metabolik:** Tubuh sudah terbiasa dengan defisit kalori saat ini. **Solusi:** Turunkan target kalori harian sebanyak 100-150 kkal atau tambah durasi jalan kaki mingguan.
                3. **Retensi Air:** Bisa jadi karena stres atau kurang tidur. Cek kualitas istirahat malam lo.
                """)
    else:
      st.success(
          f"🎉 **Progres Bagus!** Berat badan turun sebanyak {abs(weight_diff):.1f}"
          " kg dalam periode ini. Pertahankan pola makan dan latihannya!"
      )
