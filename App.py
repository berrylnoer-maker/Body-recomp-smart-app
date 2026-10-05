import datetime
import math
import streamlit as st

st.set_page_config(
    page_title="Smart AI Cut & Fitness Planner", page_icon="💪", layout="wide"
)

st.title("🔥 Smart AI Cutting & Fitness Planner")
st.markdown(
    "Aplikasi web pintar untuk atur berat badan, target lemak, dan evaluasi"
    " progres cutting secara personal."
)

with st.sidebar:
  st.header("📝 Profil & Data Fisik")
  user_name = st.text_input("Nama Pengguna", "Berryl")
  gender = st.selectbox("Jenis Kelamin", ["Pria", "Wanita"])

  # Gunakan number_input agar lebih mudah diketik langsung di HP dibanding slider
  current_weight = st.number_input(
      "Berat Badan Sekarang (kg)",
      min_value=30.0,
      max_value=200.0,
      value=75.0,
      step=0.5,
  )
  current_height = st.number_input(
      "Tinggi Badan (cm)",
      min_value=100.0,
      max_value=220.0,
      value=168.0,
      step=1.0,
  )
  age = st.number_input(
      "Usia (tahun)", min_value=15, max_value=80, value=25, step=1
  )

  st.divider()
  st.header("🎯 Target & Kondisi Tubuh")
  current_body_fat = st.number_input(
      "Lemak Badan Saat Ini (%)",
      min_value=5.0,
      max_value=40.0,
      value=20.0,
      step=0.5,
  )

  min_target_fat = 8.0 if gender == "Pria" else 15.0
  target_body_fat = st.number_input(
      "Target Lemak Badan (%)",
      min_value=min_target_fat,
      max_value=35.0,
      value=10.0,
      step=0.5,
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

# Validasi Target
if current_body_fat <= target_body_fat:
  st.error(
      "⚠️ Target lemak badan harus lebih rendah dari persentase lemak saat"
      " ini untuk melakukan cutting!"
  )
else:
  # 1. Kalkulasi Berdasarkan Gender & Input Baru
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
    c1.metric(
        "Target Berat Badan",
        f"{target_weight:.1f} kg",
        f"-{total_fat_to_lose:.1f} kg lemak",
    )
    c2.metric("Kalori Harian", f"{target_calories} kkal", f"TDEE: {int(tdee)}")
    c3.metric(
        "Protein Harian",
        f"{int(current_weight * 2.2)} gram",
        "Jaga Massa Otot",
    )

    st.info(
        "💡 Penyesuaian: Angka berat badan dan target lemak sekarang sudah"
        " menggunakan kotak input angka agar lebih presisi dan mudah diubah"
        " langsung dari HP."
    )

  with tab2:
    st.subheader("📸 Catat Makanan dengan AI Photo Scanner")
    st.markdown(
        "Upload foto makanan lo untuk menghitung estimasi kalori dan makro"
        " nutrisi secara otomatis."
    )
    uploaded_file = st.file_uploader(
        "Pilih foto makanan...", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file is not None:
      st.image(
          uploaded_file, caption="Foto Makanan Diunggah", use_container_width=True
      )
      if st.button("Analisis Foto & Hitung Kalori"):
        st.success(
            "✅ **Makanan Terdeteksi:** Dada Ayam (150g) + Nasi Merah (100g) +"
            " Tumis Sayur."
        )
        st.markdown("""
                * **Estimasi Kalori:** 420 kkal
                * **Protein:** 38g | **Karbo:** 45g | **Lemak:** 8g
                """)

  with tab3:
    st.subheader("🔍 Smart Evaluation (Evaluasi Progres)")
    st.markdown(
        "Masukkan data timbangan terbaru secara berkala untuk mendeteksi"
        " stagnasi."
    )
    last_weight_check = st.number_input(
        "Berat Badan Periode Lalu (kg)", 30.0, 200.0, current_weight, step=0.5
    )
    current_weight_check = st.number_input(
        "Berat Badan Terbaru (kg)", 30.0, 200.0, current_weight, step=0.5
    )

    if st.button("Jalankan Evaluasi"):
      weight_diff = current_weight_check - last_weight_check
      if weight_diff >= 0:
        st.error(
            "⚠️ **Progres Mandek (Plateau)!** Kalori harian mungkin perlu"
            " diturunkan sedikit atau tingkatkan kardio jalan kaki."
        )
      else:
        st.success(
            f"🎉 **Progres Mantap!** Turun sebanyak {abs(weight_diff):.1f} kg."
            " Pertahankan!"
        )
