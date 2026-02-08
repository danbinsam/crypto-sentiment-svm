import streamlit as st
import joblib
import os
import re

# --- 1. Konfigurasi Halaman (Dark Mode Only) ---
st.set_page_config(
    page_title="Analisis Sentimen Aplikasi Crypto",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. Custom CSS (Dark Mode with Binance Yellow - No Glow) ---
st.markdown("""
<style>
    /* Import Google Font untuk typography modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Dark Background seperti Binance */
    .stApp {
        background: #181a20;
    }
    
    /* Mengatur padding halaman agar lebih lega */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 4rem;
        max-width: 1000px;
    }
    
    /* Hide default h1 */
    h1 {
        display: none;
    }
    
    /* Custom Title dengan split color */
    .custom-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 2.8rem;
        letter-spacing: -0.5px;
    }
    
    .title-normal {
        color: #EAECEF;
    }
    
    .title-highlight {
        color: #F0B90B;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #848E9C;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    /* Styling Text Area - No Glow */
    .stTextArea textarea {
        border-radius: 20px;
        border: 2px solid #2B3139 !important;
        padding: 20px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: #1E2329 !important;
        color: #EAECEF !important;
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #848E9C !important;
        opacity: 0.7;
    }
    
    .stTextArea textarea:focus {
        border-color: #F0B90B !important;
        outline: none !important;
    }
    
    /* Hilangkan outline hitam dari label */
    .stTextArea label {
        color: #EAECEF !important;
    }
    
    /* Styling Tombol dengan BINANCE YELLOW - No Glow */
    .stButton > button,
    .stButton button,
    button[kind="primary"],
    button[kind="secondary"] {
        width: 100% !important;
        border-radius: 16px !important;
        background: #F0B90B !important;
        background-color: #F0B90B !important;
        color: #181a20 !important;
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px !important;
        outline: none !important;
    }
    
    .stButton > button:hover,
    .stButton button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover {
        background: #FCD535 !important;
        background-color: #FCD535 !important;
        transform: translateY(-2px) !important;
        border: none !important;
        color: #181a20 !important;
    }
    
    .stButton > button:active,
    .stButton button:active {
        transform: translateY(0) !important;
        background: #F0B90B !important;
        background-color: #F0B90B !important;
    }
    
    .stButton > button:focus,
    .stButton button:focus {
        outline: none !important;
        border: none !important;
        background: #F0B90B !important;
        background-color: #F0B90B !important;
    }
    
    /* Override semua style default Streamlit button */
    [data-testid="stForm"] button {
        background: #F0B90B !important;
        background-color: #F0B90B !important;
        color: #181a20 !important;
    }

    /* Styling Kartu Hasil (Cards) - Dark Theme, No Glow */
    div[data-testid="stMetricValue"] {
        font-size: 1.2rem;
    }
    
    .result-card {
        background: #1E2329;
        padding: 28px 20px;
        border-radius: 24px;
        border: 2px solid #2B3139;
        text-align: center;
        margin-bottom: 10px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: #F0B90B;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-8px);
        border-color: #F0B90B;
    }
    
    .result-card:hover::before {
        opacity: 1;
    }
    
    .exchange-name {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #F0B90B;
        font-weight: 700;
        margin-bottom: 14px;
    }
    
    .sentiment-label {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    
    /* Warna sentimen SOFT - hanya POSITIF dan NEGATIF */
    .positive { 
        color: #2EBD85;
    }
    .negative { 
        color: #F6465D;
    }
    
    /* Circle Indicator - lingkaran dengan warna sentimen, No Glow */
    .circle-indicator {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        margin: 12px auto 0;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.5s ease;
    }
    
    .circle-positive {
        background: #2EBD85;
    }
    
    .circle-negative {
        background: #F6465D;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Divider dengan gradien */
    hr {
        margin: 3rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #2B3139, transparent);
    }
    
    /* Section header */
    .section-header {
        text-align: center;
        color: #EAECEF;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        letter-spacing: -0.3px;
    }
    
    /* Warning styling */
    .stAlert {
        border-radius: 16px;
        border: none !important;
        background: #2B3139 !important;
        color: #EAECEF !important;
    }
    
    /* Form styling */
    [data-testid="stForm"] {
        background: #1E2329;
        padding: 2rem;
        border-radius: 24px;
        border: 2px solid #2B3139;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #848E9C;
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    .footer-highlight {
        color: #F0B90B;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Fungsi Preprocessing ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.strip()
    return text

# --- 4. Load Semua Model Sekaligus ---
@st.cache_resource
def load_all_models():
    base_path = "models"
    # Daftar nama file yang sesuai di folder models
    exchanges = ["Indodax", "Tokocrypto", "Pintu", "Combined"]
    loaded_assets = {}
    
    for ex in exchanges:
        try:
            m_path = os.path.join(base_path, f"{ex}_model.pkl")
            v_path = os.path.join(base_path, f"{ex}_vectorizer.pkl")
            
            model = joblib.load(m_path)
            vect = joblib.load(v_path)
            loaded_assets[ex] = (model, vect)
        except FileNotFoundError:
            st.error(f"⚠️ File model/vectorizer untuk {ex} tidak ditemukan.")
    
    return loaded_assets

# Load assets di awal
assets = load_all_models()

# --- 5. User Interface (UI) ---
# Custom Title dengan split color
st.markdown('''
<div class="custom-title">
    <span class="title-normal">📊 Analisis Sentimen </span><span class="title-highlight">Aplikasi Crypto</span>
</div>
''', unsafe_allow_html=True)

st.markdown('<p class="subtitle">Analisis sentimen menggunakan 4 model SVM terlatih untuk platform crypto Indonesia</p>', unsafe_allow_html=True)

# Input Form
with st.form(key='sentiment_form'):
    user_input = st.text_area(
        "Tulis ulasan Anda di sini...", 
        height=120, 
        placeholder="Contoh: Aplikasinya lancar dan fitur lengkap, sangat membantu untuk trading crypto.",
        label_visibility="collapsed"
    )
    submit_button = st.form_submit_button(label='✨ Analisis Sentimen Sekarang')

# --- 6. Logika Eksekusi & Tampilan Hasil ---
if submit_button and user_input:
    cleaned_text = clean_text(user_input)
    
    st.markdown("---")
    st.markdown('<div class="section-header">📊 Hasil Analisis Sentimen</div>', unsafe_allow_html=True)
    
    # Membuat 4 kolom untuk hasil (Grid Layout)
    cols = st.columns(4)
    
    # Loop untuk setiap exchange dan tampilkan di kolom masing-masing
    # Urutan: Indodax, Tokocrypto, Pintu, Combined
    target_exchanges = ["Indodax", "Tokocrypto", "Pintu", "Combined"]
    
    for idx, ex_name in enumerate(target_exchanges):
        if ex_name in assets:
            model, vectorizer = assets[ex_name]
            
            # Prediksi
            text_vector = vectorizer.transform([cleaned_text])
            prediction = model.predict(text_vector)[0]
            
            # Tentukan Label & Warna CSS - HANYA POSITIF atau NEGATIF
            label_text = ""
            css_class = ""
            circle_class = ""
            
            # Logika label - hanya 2 kemungkinan: POSITIF atau NEGATIF
            if prediction == 1 or prediction == "positive":
                label_text = "POSITIF"
                css_class = "positive"
                circle_class = "circle-positive"
            else:  # prediction == 0 or -1 or "negative"
                label_text = "NEGATIF"
                css_class = "negative"
                circle_class = "circle-negative"
            
            # Tampilkan Card di Kolom dengan lingkaran warna
            with cols[idx]:
                st.markdown(f"""
                <div class="result-card">
                    <div class="exchange-name">{ex_name}</div>
                    <div class="sentiment-label {css_class}">{label_text}</div>
                    <div class="circle-indicator {circle_class}"></div>
                </div>
                """, unsafe_allow_html=True)
                
elif submit_button and not user_input:
    st.warning("⚠️ Harap masukkan teks ulasan terlebih dahulu.")

# Footer
st.markdown("---")
st.markdown('<p class="footer">Dibuat dengan <span class="footer-highlight">Machine Learning</span> menggunakan Streamlit</p>', unsafe_allow_html=True)