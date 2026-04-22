import streamlit as st
import pandas as pd
import os

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Axioo Laptop Finder",
    page_icon="💻",
    layout="wide"
)

# --- FUNGSI TAMPILKAN LOGO ---
def tampilkan_logo(lebar=150):
    path_logo = "logo_axioo.png" 
    if os.path.exists(path_logo):
        st.image(path_logo, width=lebar)
    else:
        # Fallback kalau file logo tidak ada
        st.markdown(f"### 💻 **AXIOO**")

# 2. DATABASE LAPTOP AXIOO (Data Lengkap & Fix URL Key)
data_laptop = [
    {
        "seri": "Axioo Hype 1",
        "procesor": "Intel Celeron",
        "ram": 4, "layar": "14 inch", 
        "harga": 2900000,
        "tipe": "Basic", 
        "rating": 4.2, 
        "gambar": "https://down-id.img.susercontent.com/file/id-11134207-7r990-lr5injffxqo967",
        "URL": "https://www.tokopedia.com/protechcom/laptop-axioo-hype-1-celeron-n4020-4gb-128gb-ssd-14-hd-windows-11-resmi-1731071902064346158"
    },
    {
        "seri": "Axioo Hype 3",
        "procesor": "Intel Core i3",
        "ram": 8, "layar": "14 inch",
        "harga": 4100000, 
        "tipe": "Office", 
        "rating": 4.5,
        "gambar" : "https://els.id/wp-content/uploads/2023/09/dd8060cb-011e-4d37-88d1-17155f34251e-1.jpg",
        "URL": "https://www.tokopedia.com/digitechmall/laptop-axioo-mybook-hype-3-g11-intel-i3-1125g4-8gb-256gb-14-fhd-ips-1732019477732099699"
    },
    {
        "seri": "Axioo Hype 5",
        "procesor": "AMD Ryzen 5",
        "ram": 8, "layar": "14 inch",
        "harga": 4900000, 
        "tipe": "Work", 
        "rating": 4.8, 
        "gambar" : "https://els.id/wp-content/uploads/2024/12/Mybook-Hype-5.png",
        "URL": "https://www.tokopedia.com/collinsofficial/laptop-axioo-hype-5-amd-x5-2-lollipop-ryzen-5-7430-8gb-256gb-14-0-fhd-ips-w11-1730825119261886272"
    },
    {
        "seri": "Axioo MyBook Z10", 
        "procesor": "Intel Core i5",
        "ram": 16, "layar": "15 inch", 
        "harga": 7500000, 
        "tipe": "Pro",
        "rating": 4.7, 
        "gambar" : "https://gizmologi.id/wp-content/uploads/2023/11/Axioo-MyBook-Z10-Metal-G13-218.jpg",
        "URL": "https://www.tokopedia.com/anugerahdigital/axioo-mybook-z10-metal-pink-only-core-i5-1335u-8-256gb-m2-win-11-ori-14-fhd-ips-1733497463629382999"
    },
    {
        "seri": "Axioo Pongo 725",
        "procesor": "Intel Core i7",
        "ram": 16, "layar": "15 inch",
        "harga": 13000000,
        "tipe": "Gaming",
        "rating": 4.9,
        "gambar": "https://gizmologi.id/wp-content/uploads/2023/03/00-1-1.jpg",
        "URL": "https://www.tokopedia.com/skytechstoreid/axioo-gaming-pongo-725-v2-intel-core-i7-13620h-ram32gb-ssd2tb-15-6-ips-144hz-rtx2050-windows-11-pro-1731541755023558446"
    },
    {
        "seri": "Axioo MyBook Z6", 
        "procesor": "Intel Core i3", 
        "ram": 8, "layar": "14 inch", 
        "harga": 3800000, 
        "tipe": "Office", 
        "rating": 4.6, 
        "gambar" : "https://els.id/wp-content/uploads/2023/09/MyBook-Z6-Grey-2.png", 
        "URL": "https://www.tokopedia.com/collinsofficial/axioo-mybook-z6-metal-i3-1215-8gb-256gb-uhd-14-0-fhd-ips-w11-non-paket-a733b"
    }
]

df = pd.DataFrame(data_laptop)

# 3. HEADER
col1, col2 = st.columns([1, 5])
with col1:
    tampilkan_logo(80)
with col2:
    st.title("Axioo Smart Selector")
    st.caption("Cari Laptop Axioo Impian Berdasarkan Budget & Rating Marketplace")

st.divider()

# 4. SIDEBAR
st.sidebar.header("⚙️ Filter")
in_budget = st.sidebar.number_input("Budget Maksimum (Rp)", 2000000, 20000000, 7000000, 100000)
in_ram = st.sidebar.selectbox("RAM Minimal (GB)", [4, 8, 16], index=1)
in_proc = st.sidebar.radio("Prosesor", ["Semua", "Intel Core", "AMD Ryzen", "Intel Celeron"])
in_tipe = st.sidebar.multiselect("Kategori", ["Basic", "Office", "Work", "Pro", "Gaming"], default=["Office", "Work"])
in_rating = st.sidebar.number_input("Minimal Rating (1-5)", 1.0, 5.0, 4.0, 0.1)

# 5. LOGIKA FILTER
rekomendasi = df[(df['harga'] <= in_budget) & 
                 (df['ram'] >= in_ram) & 
                 (df['rating'] >= in_rating)]

if in_proc != "Semua":
    rekomendasi = rekomendasi[rekomendasi['procesor'].str.contains(in_proc)]

if in_tipe:
    rekomendasi = rekomendasi[rekomendasi['tipe'].isin(in_tipe)]

# 6. TAMPILAN UTAMA
st.subheader(f"✅ {len(rekomendasi)} Rekomendasi Ditemukan")

if not rekomendasi.empty:
    for i, row in rekomendasi.iterrows():
        with st.expander(f" {row['seri']} - Rp{row['harga']:,}"):
            c_img, c_txt = st.columns([1, 2])
            
            with c_img:
                st.image(row['gambar'], use_container_width=True)
            
            with c_txt:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Spesifikasi:**")
                    st.write(f" {row['procesor']}")
                    st.write(f" RAM {row['ram']}GB")
                    st.write(f" {row['layar']}")
                with col_b:
                    st.write("**Kesan Pembeli:**")
                    st.write(f" {row['rating']} / 5.0")
                    st.write(f" Tipe: {row['tipe']}")
                
                st.divider()
                
                # FIX: Memastikan memanggil kolom 'URL' (Huruf Besar)
                st.link_button(
                    f"🛒 Lihat di Tokopedia", 
                    row['URL'], 
                    type="primary", 
                    use_container_width=True
                )
else:
    st.info("Pencarian tidak ditemukan. Coba longgarkan filter Anda.")
