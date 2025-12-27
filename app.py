import streamlit as st

# --- การตกแต่งสี Red-Blue-Green & White Text ---
st.markdown("""
    <style>
    /* 1. พื้นหลังหลัก: น้ำเงินเข้มไล่เฉดไปดำ (Blue to Black) */
    .stApp {
        background: linear-gradient(180deg, #000044 0%, #000000 100%) !important;
    }
    
    /* 2. ตัวหนังสือทุกจุด: สีขาวบริสุทธิ์ (White) */
    h1, h2, h3, p, span, label, div, .stMarkdown {
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px #000000;
    }

    /* 3. ช่องกรอกข้อมูล: พื้นหลังดำ ขอบเขียวมินต์ ตัวหนังสือขาว */
    .stTextArea textarea, .stTextInput input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #00FFCC !important;
        border-radius: 10px;
    }
    
    /* 4. ปุ่ม ACTIVATE: สีแดง (Red) ตัวหนังสือขาว */
    .stButton>button {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 15px;
        height: 60px;
        width: 100%;
        font-size: 24px !important;
        font-weight: bold;
        box-shadow: 0px 0px 20px rgba(255, 0, 0, 0.5);
        transition: 0.5s;
    }

    /* 5. เอฟเฟกต์เมื่อวางเมาส์ที่ปุ่ม: เรืองแสงสีเขียว */
    .stButton>button:hover {
        background-color: #00FF00 !important;
        color: #000000 !important;
        box-shadow: 0px 0px 25px rgba(0, 255, 0, 0.8);
    }

    /* 6. แถบสถานะ Metric: พื้นหลังน้ำเงิน ขอบขาว */
    div[data-testid="metric-container"] {
        background-color: rgba(0, 0, 100, 0.5) !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 10px;
        padding: 10px;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนแสดงผลหลัก ---
try:
    st.image("1000008780.jpg", use_container_width=True)
except:
    st.title("💎 SYNAPSE 6D ENERGY PRO")

st.subheader("อยู่นิ่งๆ ไม่เจ็บตัว")

# ช่องรับข้อมูลที่ตอนนี้ขอบจะเป็นสีเขียว ตัวหนังสือขาว
mood = st.text_input("ระบุสภาวะจิตใจของคุณ:", placeholder="เบื่อเซ่ง / ต้องการพลัง...")

if st.button("🚀 ACTIVATE ENERGY"):
    st.write("ระบบกำลังจูนคลื่นความถี่น้ำเงิน-แดง-เขียวให้คุณ...")
    # โค้ดประมวลผลเสียง R&B ของคุณจะทำงานต่อตรงนี้
