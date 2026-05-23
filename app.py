import re
import string
import html
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="Shopee Satisfaction Analysis",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(255, 100, 50, 0.28), transparent 28%),
            radial-gradient(circle at 90% 20%, rgba(255, 184, 77, 0.22), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(255, 106, 61, 0.16), transparent 32%),
            linear-gradient(135deg, #fff7f0 0%, #fffdf8 42%, #fff1e6 100%);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2a1710 0%, #3b2117 55%, #1f130f 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] * {
        color: #fff7f1 !important;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 16px;
    }

    .sidebar-title {
        font-size: 24px;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        line-height: 1.6;
        opacity: 0.85;
    }

    .hero {
        background:
            linear-gradient(135deg, rgba(255, 92, 38, 0.96), rgba(255, 132, 55, 0.95), rgba(255, 184, 77, 0.92)),
            url("https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?q=80&w=1600&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        color: white;
        border-radius: 34px;
        padding: 42px 44px;
        box-shadow: 0 30px 70px rgba(255, 92, 38, 0.28);
        position: relative;
        overflow: hidden;
        margin-bottom: 28px;
    }

    .hero::before {
        content: "";
        position: absolute;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.18);
        right: -120px;
        top: -130px;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.12);
        right: 170px;
        bottom: -90px;
    }

    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 820px;
    }

    .hero-badge {
        display: inline-flex;
        padding: 9px 15px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.22);
        border: 1px solid rgba(255, 255, 255, 0.35);
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 18px;
        backdrop-filter: blur(10px);
    }

    .hero-title {
        font-size: 46px;
        line-height: 1.1;
        font-weight: 900;
        letter-spacing: -1.2px;
        margin-bottom: 16px;
    }

    .hero-desc {
        font-size: 17px;
        line-height: 1.8;
        opacity: 0.95;
        max-width: 760px;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin-bottom: 28px;
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(255, 111, 53, 0.16);
        border-radius: 26px;
        padding: 24px;
        box-shadow: 0 18px 45px rgba(97, 57, 35, 0.10);
        backdrop-filter: blur(16px);
        transition: all 0.22s ease;
    }

    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 26px 58px rgba(97, 57, 35, 0.14);
    }

    .stat-icon {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        background: linear-gradient(135deg, #ff6b35, #ffb347);
        color: white;
        font-size: 24px;
        margin-bottom: 14px;
        box-shadow: 0 12px 26px rgba(255, 107, 53, 0.24);
    }

    .stat-label {
        font-size: 13px;
        font-weight: 800;
        color: #9a6a54;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .stat-value {
        font-size: 22px;
        font-weight: 900;
        color: #2b1c16;
    }

    .panel {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(255, 111, 53, 0.16);
        border-radius: 30px;
        padding: 28px;
        box-shadow: 0 20px 55px rgba(97, 57, 35, 0.10);
        backdrop-filter: blur(18px);
        margin-bottom: 24px;
    }

    .panel-title {
        font-size: 24px;
        font-weight: 900;
        color: #281b15;
        margin-bottom: 8px;
    }

    .panel-desc {
        color: #7c5f51;
        font-size: 14.5px;
        line-height: 1.8;
        margin-bottom: 18px;
    }

    .mini-card {
        background: linear-gradient(180deg, #ffffff, #fff8f3);
        border: 1px solid rgba(255, 111, 53, 0.14);
        border-radius: 22px;
        padding: 20px;
        margin-bottom: 16px;
    }

    .mini-title {
        font-size: 16px;
        font-weight: 900;
        color: #2d1e18;
        margin-bottom: 8px;
    }

    .mini-desc {
        font-size: 14px;
        color: #7c5f51;
        line-height: 1.7;
    }

    .tag {
        display: inline-block;
        padding: 8px 12px;
        border-radius: 999px;
        background: #fff0e7;
        color: #f05a28;
        font-size: 13px;
        font-weight: 800;
        border: 1px solid rgba(240, 90, 40, 0.16);
        margin-right: 8px;
        margin-bottom: 8px;
    }

    div.stButton > button {
        width: 100%;
        height: 3.4rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #ff5f2e 0%, #ff8b3d 60%, #ffb347 100%);
        color: white;
        font-weight: 900;
        font-size: 16px;
        border: none;
        box-shadow: 0 16px 34px rgba(255, 95, 46, 0.28);
        transition: all 0.22s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 22px 42px rgba(255, 95, 46, 0.36);
        color: white;
        border: none;
    }

    textarea {
        border-radius: 20px !important;
        border: 1px solid rgba(255, 111, 53, 0.24) !important;
        background: rgba(255, 255, 255, 0.90) !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 16px;
        border-color: rgba(255, 111, 53, 0.24);
        background: rgba(255, 255, 255, 0.94);
    }

    .result-card {
        border-radius: 32px;
        padding: 30px;
        margin-top: 18px;
        margin-bottom: 24px;
        box-shadow: 0 24px 60px rgba(97, 57, 35, 0.13);
        position: relative;
        overflow: hidden;
    }

    .result-card::after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        right: -75px;
        top: -75px;
        background: rgba(255, 255, 255, 0.45);
    }

    .result-puas {
        background: linear-gradient(135deg, #e9fff2 0%, #f7fffb 100%);
        border: 1px solid rgba(22, 163, 74, 0.24);
    }

    .result-tidak {
        background: linear-gradient(135deg, #fff0f0 0%, #fffafa 100%);
        border: 1px solid rgba(220, 38, 38, 0.22);
    }

    .result-netral {
        background: linear-gradient(135deg, #fff8e5 0%, #fffdf6 100%);
        border: 1px solid rgba(245, 158, 11, 0.24);
    }

    .result-label {
        position: relative;
        z-index: 2;
        font-size: 13px;
        color: #7c5f51;
        font-weight: 900;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .result-main {
        position: relative;
        z-index: 2;
        font-size: 38px;
        font-weight: 950;
        color: #241712;
        margin-bottom: 10px;
        letter-spacing: -0.6px;
    }

    .result-desc {
        position: relative;
        z-index: 2;
        color: #6f574c;
        line-height: 1.8;
        font-size: 15px;
        max-width: 760px;
    }

    .preprocess-box {
        background: linear-gradient(135deg, #241915, #34231c);
        color: #ffe7d9;
        border-radius: 22px;
        padding: 20px 22px;
        font-size: 14px;
        line-height: 1.8;
        overflow-wrap: break-word;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .prob-row {
        margin-bottom: 18px;
    }

    .prob-top {
        display: flex;
        justify-content: space-between;
        font-weight: 900;
        color: #2b1c16;
        margin-bottom: 8px;
        font-size: 14px;
    }

    .prob-track {
        width: 100%;
        height: 14px;
        background: #f1ddd2;
        border-radius: 999px;
        overflow: hidden;
        box-shadow: inset 0 2px 5px rgba(68, 38, 24, 0.08);
    }

    .prob-fill {
        height: 100%;
        border-radius: 999px;
    }

    .fill-puas {
        background: linear-gradient(90deg, #16a34a, #86efac);
    }

    .fill-tidak {
        background: linear-gradient(90deg, #dc2626, #fca5a5);
    }

    .fill-netral {
        background: linear-gradient(90deg, #f59e0b, #fde68a);
    }

    .footer {
        text-align: center;
        color: #8b6c5e;
        font-size: 13px;
        padding: 26px 0 6px;
    }

    @media screen and (max-width: 900px) {
        .hero-title {
            font-size: 34px;
        }

        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PREPROCESSING TEKS
# ============================================================

STOPWORDS = {
    "shopee", "shoppe", "apk", "aplikasi", "app", "nya", "yg", "yang",
    "di", "ke", "dari", "dan", "ini", "itu", "saya", "aku", "kami",
    "kamu", "anda", "buat", "banget", "sih", "nih", "dong", "deh",
    "lah", "pun", "para", "pada", "untuk", "dengan", "dalam", "atau",
    "karena", "sebagai", "adalah", "jadi", "juga", "ada", "sudah",
    "belum", "bisa", "lebih", "sangat", "sekali", "terlalu", "semua",
    "akan", "agar", "oleh", "kalau", "kalo", "ya", "oh", "min"
}

NORMALISASI_KATA = {
    "gk": "tidak",
    "ga": "tidak",
    "gak": "tidak",
    "nggak": "tidak",
    "ngga": "tidak",
    "tdk": "tidak",
    "dak": "tidak",
    "tak": "tidak",
    "bgt": "banget",
    "bgtt": "banget",
    "mantul": "mantap",
    "lemot": "lambat",
    "lelet": "lambat",
    "ngelag": "lambat",
    "lag": "lambat",
    "eror": "error",
    "err": "error",
    "apk": "aplikasi",
    "app": "aplikasi",
    "cs": "customer service",
    "ongkir": "ongkos kirim",
    "gratisongkir": "gratis ongkir",
    "cod": "bayar ditempat",
    "checkout": "cekout",
    "co": "cekout",
    "login": "masuk",
    "loggin": "masuk",
    "gabisa": "tidak bisa",
    "gbs": "tidak bisa"
}


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"@[A-Za-z0-9_]+|#[A-Za-z0-9_]+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = text.split()
    tokens = [NORMALISASI_KATA.get(token, token) for token in tokens]
    tokens = [word for word in tokens if word not in STOPWORDS and len(word) > 1]

    return " ".join(tokens)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    base_dir = Path(__file__).parent
    model_path = base_dir / "model_kepuasan_shopee_naive_bayes.pkl"

    if not model_path.exists():
        st.error(
            "File model tidak ditemukan. Pastikan file "
            "`model_kepuasan_shopee_naive_bayes.pkl` berada satu folder dengan `app.py`."
        )
        st.stop()

    if model_path.stat().st_size == 0:
        st.error(
            "File model ditemukan, tetapi ukurannya 0 KB. "
            "Artinya file model kosong atau rusak. Silakan ganti dengan file model `.pkl` yang benar."
        )
        st.stop()

    try:
        return joblib.load(model_path)
    except Exception as e:
        st.error("Model gagal dimuat. Pastikan file `.pkl` tidak rusak.")
        st.code(str(e))
        st.stop()


model = load_model()


# ============================================================
# HELPER UI
# ============================================================

def result_style(label):
    if label == "Puas":
        return {
            "emoji": "😊",
            "class": "result-puas",
            "title": "Pengguna Cenderung Puas",
            "desc": "Ulasan ini menunjukkan pengalaman pengguna yang positif terhadap aplikasi Shopee."
        }

    if label == "Tidak Puas":
        return {
            "emoji": "😟",
            "class": "result-tidak",
            "title": "Pengguna Cenderung Tidak Puas",
            "desc": "Ulasan ini menunjukkan adanya keluhan atau pengalaman negatif dari pengguna."
        }

    return {
        "emoji": "😐",
        "class": "result-netral",
        "title": "Pengguna Cenderung Cukup Puas",
        "desc": "Ulasan ini berada pada kategori netral atau cukup puas."
    }


def bar_class(label):
    if label == "Puas":
        return "fill-puas"
    if label == "Tidak Puas":
        return "fill-tidak"
    return "fill-netral"


def probability_bars(df_prob):
    for _, row in df_prob.iterrows():
        label = str(row["Label"])
        persen = float(row["Probabilitas (%)"])

        st.markdown(
            f"""
            <div class="prob-row">
                <div class="prob-top">
                    <span>{html.escape(label)}</span>
                    <span>{persen:.2f}%</span>
                </div>
                <div class="prob-track">
                    <div class="prob-fill {bar_class(label)}" style="width: {persen}%;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">🛒 Shopee AI</div>
            <div class="sidebar-subtitle">
                Dashboard prediksi kepuasan pengguna berdasarkan ulasan aplikasi Shopee.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔍 Metode")
    st.write("TF-IDF Vectorizer")
    st.write("Multinomial Naive Bayes")

    st.markdown("---")

    st.markdown("### 🏷️ Label")
    st.write("🟢 Rating 4–5: Puas")
    st.write("🟡 Rating 3: Cukup Puas")
    st.write("🔴 Rating 1–2: Tidak Puas")

    st.markdown("---")
    st.caption("Proyek Data Mining")


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="hero-badge">✨ Data Mining • Sentiment Analysis • Machine Learning</div>
            <div class="hero-title">Analisis Kepuasan Pengguna Aplikasi Shopee</div>
            <div class="hero-desc">
                Sistem prediksi kepuasan pengguna berbasis ulasan teks menggunakan 
                TF-IDF dan algoritma Multinomial Naive Bayes. Masukkan ulasan, 
                lalu sistem akan mengklasifikasikan opini menjadi Puas, Cukup Puas, 
                atau Tidak Puas.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# STAT CARDS
# ============================================================

st.markdown(
    """
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon">🧹</div>
            <div class="stat-label">Tahap Pertama</div>
            <div class="stat-value">Preprocessing Teks</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🔢</div>
            <div class="stat-label">Ekstraksi Fitur</div>
            <div class="stat-value">TF-IDF</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🤖</div>
            <div class="stat-label">Algoritma Model</div>
            <div class="stat-value">Naive Bayes</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INPUT SECTION
# ============================================================

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">📝 Input Ulasan Pengguna</div>
            <div class="panel-desc">
                Tulis ulasan pengguna aplikasi Shopee pada kolom di bawah ini.
                Sistem akan membersihkan teks dan memprediksi tingkat kepuasan pengguna.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    contoh_ulasan = st.selectbox(
        "Pilih contoh ulasan",
        [
            "",
            "Aplikasi Shopee sangat bagus, mudah digunakan, dan pengiriman cepat.",
            "Aplikasi sering error, lemot, dan voucher tidak bisa digunakan.",
            "Lumayan bagus, tetapi kadang masih lambat saat checkout.",
            "Barang tidak sampai, kurir lama, dan customer service tidak membantu."
        ]
    )

    ulasan = st.text_area(
        "Masukkan teks ulasan",
        value=contoh_ulasan,
        height=190,
        placeholder="Contoh: Aplikasi bagus, mudah digunakan, pengiriman cepat, dan banyak promo..."
    )

    tombol_prediksi = st.button("🔍 Prediksi Kepuasan")

with right:
    st.markdown(
        """
        <div class="mini-card">
            <div class="mini-title">📌 Kategori Prediksi</div>
            <div class="mini-desc">
                Model akan mengklasifikasikan ulasan ke dalam tiga kategori utama.
            </div>
            <br>
            <span class="tag">Puas</span>
            <span class="tag">Cukup Puas</span>
            <span class="tag">Tidak Puas</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="mini-card">
            <div class="mini-title">⚙️ Alur Sistem</div>
            <div class="mini-desc">
                1. Input ulasan pengguna<br>
                2. Preprocessing teks<br>
                3. Transformasi TF-IDF<br>
                4. Prediksi Naive Bayes<br>
                5. Tampilkan hasil
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="mini-card">
            <div class="mini-title">🎯 Tujuan</div>
            <div class="mini-desc">
                Membantu menganalisis kepuasan pengguna aplikasi Shopee berdasarkan review.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HASIL PREDIKSI
# ============================================================

if tombol_prediksi:
    if ulasan.strip() == "":
        st.warning("Silakan masukkan ulasan terlebih dahulu.")
    else:
        ulasan_bersih = clean_text(ulasan)

        if ulasan_bersih.strip() == "":
            st.warning("Teks terlalu pendek atau tidak memiliki kata penting setelah preprocessing.")
        else:
            prediksi = model.predict([ulasan_bersih])[0]
            style = result_style(prediksi)

            st.markdown(
                f"""
                <div class="result-card {style["class"]}">
                    <div class="result-label">Hasil Prediksi</div>
                    <div class="result-main">{style["emoji"]} {html.escape(str(prediksi))}</div>
                    <div class="result-desc">
                        <b>{style["title"]}</b><br>
                        {style["desc"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            result_left, result_right = st.columns([1, 1], gap="large")

            with result_left:
                st.markdown(
                    """
                    <div class="panel">
                        <div class="panel-title">🧾 Teks Setelah Preprocessing</div>
                        <div class="panel-desc">
                            Teks berikut adalah hasil pembersihan dari huruf kapital, angka, simbol, tanda baca, dan stopword.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="preprocess-box">
                        {html.escape(ulasan_bersih)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with result_right:
                st.markdown(
                    """
                    <div class="panel">
                        <div class="panel-title">📊 Probabilitas Model</div>
                        <div class="panel-desc">
                            Semakin besar persentase, semakin tinggi keyakinan model terhadap label tersebut.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if hasattr(model, "predict_proba"):
                    probabilitas = model.predict_proba([ulasan_bersih])[0]

                    df_prob = pd.DataFrame({
                        "Label": model.classes_,
                        "Probabilitas": probabilitas
                    })

                    df_prob["Probabilitas (%)"] = (df_prob["Probabilitas"] * 100).round(2)
                    df_prob = df_prob.sort_values(by="Probabilitas", ascending=False)

                    probability_bars(df_prob)

                    with st.expander("Lihat tabel probabilitas"):
                        st.dataframe(
                            df_prob[["Label", "Probabilitas (%)"]],
                            use_container_width=True
                        )


# ============================================================
# TENTANG MODEL
# ============================================================

st.markdown("---")

with st.expander("📚 Tentang Model dan Penelitian"):
    st.write(
        """
        Aplikasi ini merupakan hasil deployment proyek data mining dengan judul:

        **Analisis Kepuasan Pengguna Aplikasi Shopee Berdasarkan Ulasan dan Rating Menggunakan Metode Data Mining**

        Model menggunakan pendekatan klasifikasi teks. Rating digunakan sebagai dasar pembuatan label kepuasan:

        - Rating 1–2 = Tidak Puas
        - Rating 3 = Cukup Puas
        - Rating 4–5 = Puas

        Teks ulasan diproses melalui tahap preprocessing, kemudian diubah menjadi fitur numerik menggunakan TF-IDF.
        Setelah itu, algoritma Multinomial Naive Bayes digunakan untuk memprediksi kategori kepuasan pengguna.
        """
    )

st.markdown(
    """
    <div class="footer">
        © 2026 • Proyek Data Mining • Analisis Kepuasan Pengguna Aplikasi Shopee
    </div>
    """,
    unsafe_allow_html=True
)