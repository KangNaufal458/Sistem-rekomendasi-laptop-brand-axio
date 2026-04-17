import streamlit as st
import pandas as pd
import os 

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Axioo Laptop Finder",
    page_icon="💻", 
    layout="wide"
)
# --- FUNGSI UNTUK MENAMPILKAN LOGO ---
def tampilkan_logo(lebar=150):
    # Nama file logo Axioo
    path_logo = "logo_axioo.png" 
    
    if os.path.exists(path_logo):
        # Jika file ada, tampilkan gambarnya
        st.image(path_logo, width=lebar)
    else:
        # Jika file tidak ada, tampilkan teks bergaya (Fallback)
        # Pakai st.markdown supaya bisa kita warnai atau tebalkan
        st.markdown(f"### 💻 **AXIOO**")
        st.caption("Official Selector")

# 2. DATABASE LAPTOP AXIOO 
data_laptop = [
    {"seri": "Axioo Hype 3", "procesor": "Intel Core i3", "ram": 8, "layar": "14 inch", "harga": 4100000, "tipe": "Office", "rating": 4.5, "gambar": "https://els.id/wp-content/uploads/2023/09/dd8060cb-011e-4d37-88d1-17155f34251e-1.jpg"},
    {"seri": "Axioo MyBook Z10", "procesor": "Intel Core i5", "ram": 16, "layar": "15 inch", "harga": 7500000, "tipe": "Pro", "rating": 4.7, "gambar": "https://gizmologi.id/wp-content/uploads/2023/11/Axioo-MyBook-Z10-Metal-G13-218.jpg"},
    # ... dst
]

df = pd.DataFrame(data_laptop)

# 3. HEADER UTAMA (Ganti Emoji Laptop dengan Logo Axioo Resmi)
col_head1, col_head2 = st.columns([1, 4])
with col_head1:
    # Tampilkan Logo Axioo Besar (width=120)
    tampilkan_logo(lebar=120)
with col_head2:
    st.title("Axioo Smart Selector")
    st.markdown("Temukan laptop Axioo terbaik berdasarkan budget dan rating marketplace.")

st.divider()

# 4. SIDEBAR (Nambah Logo di atas Filter)
with st.sidebar:
    # Tampilkan Logo Axioo Kecil (width=80)
    tampilkan_logo(lebar=80)
    st.header("Filter Pencarian")
    st.markdown("---")

    # Input 1: Budget (Sama seperti sebelumnya)
    in_budget = st.sidebar.number_input(
        "1. Budget Maksimum (Rp)", 
        min_value=2000000, 
        max_value=20000000, 
        value=7000000, 
        step=100000,
        help="Ketik nominal budget kamu (Contoh: 5000000)"
    )
    
    # ... (Input sidebar lainnya tetap sama) ...
    in_ram = st.sidebar.selectbox("2. Kapasitas RAM Minimal (GB)", [4, 8, 16], index=1)
    in_proc = st.sidebar.radio("3. Preferensi Prosesor", ["Semua", "Intel Core", "AMD Ryzen", "Intel Celeron"])
    in_tipe = st.sidebar.multiselect("4. Kategori Laptop", ["Basic", "Office", "Work", "Pro", "Gaming"], default=["Office", "Work"])
    in_rating = st.sidebar.slider("5. Minimal Rating Pembeli (Bintang)", 1.0, 5.0, 4.5, step=0.1)


# 5. LOGIKA FILTER (Sama seperti sebelumnya)
rekomendasi = df[(df['harga'] <= in_budget) & 
                 (df['ram'] >= in_ram) & 
                 (df['rating'] >= in_rating)]

if in_proc != "Semua":
    rekomendasi = rekomendasi[rekomendasi['procesor'].str.contains(in_proc)]

if in_tipe:
    rekomendasi = rekomendasi[rekomendasi['tipe'].isin(in_tipe)]

# 6. TAMPILAN UTAMA (Sama seperti sebelumnya)
if in_budget < 3500000 and in_ram >= 8:
    st.error(" **Peringatan Logika:** Budget 3 jutaan untuk unit baru RAM 8GB sulit ditemukan. Coba sesuaikan budget atau rating.")
else:
    st.subheader(f" Hasil Rekomendasi (Rating > {in_rating} ⭐)")
    
    if not rekomendasi.empty:
        for i, row in rekomendasi.iterrows():
            with st.expander(f"📦 {row['seri']} - Rp{row['harga']:,}"):
                col_gambar, col_spek = st.columns([1, 2])
                with col_gambar:
                    st.image(row['gambar'], use_container_width=True)
                with col_spek:
                    # layout detail tetap sama
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("##### 🚀 Spesifikasi")
                        st.write(f"🧠 {row['procesor']} | ⚡ {row['ram']} GB | 🖥️ {row['layar']}")
                    with c2:
                        st.markdown("##### ⭐ Penilaian")
                        st.write(f"**Rating:** {row['rating']} / 5.0")
                        st.write("⭐" * int(row['rating']))
                        st.write(f"🏷️ Kategori: {row['tipe']}")
                    st.divider()
                    st.button(f"Lihat Detail {row['seri']}", key=f"btn_{i}", type="primary", use_container_width=True)
    else:
        st.info(" Tidak ada laptop yang cocok dengan kriteria filter Anda. Coba kurangi minimal rating atau naikkan budget.")

# 7. FOOTER
st.markdown("---")
st.caption("Aplikasi Rekomendasi Laptop Axioo - Dibuat dengan Streamlit & Python")