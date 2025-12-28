import streamlit as st
import google.generativeai as genai
import time

# --- การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="SYNAPSE 6D ENERGY PRO", page_icon="💎", layout="centered")

# --- ชุดคำสั่งตกแต่งดีไซน์ (CSS) โทน น้ำเงิน-แดง-ขาว ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #4d0000 100%);
        color: #ffffff;
    }
    .title-text {
        text-align: center;
        font-size: 55px;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 3px 3px 0px #ff0000, -3px -3px 0px #0000ff;
        margin-bottom: 5px;
    }
    .slogan {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #000000;
        border: 3px solid #ff0000;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(90deg, #ff0000, #ffffff, #0000ff);
        color: #000000;
        border-radius: 5px;
        font-weight: 900;
        font-size: 20px;
        width: 100%;
        border: 2px solid #000000;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนหัวแอป ---
st.markdown('<p class="title-text">💎 SYNAPSE 6D ENERGY PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="slogan">"อยู่นิ่งๆ ไม่เจ็บตัว"</p>', unsafe_allow_html=True)

# --- ส่วนรับข้อมูล ---
user_input = st.text_input("ระบุข้อความเพื่อรับพลังงาน 6D...")

if st.button("🔥 ACTIVATE ENERGY"):
    if user_input:
        with st.spinner('⚡ กำลังดึงพลังงาน น้ำเงิน-แดง-ขาว...'):
            try:
                # ระบบ AI (ใช้ Key เดิมของพี่)
                genai.configure(api_key="AIzaSyA-xxxxxx") 
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"ตอบคำถามนี้ในฐานะ SYNAPSE 6D ENERGY PRO ด้วยสไตล์ 'อยู่นิ่งๆ ไม่เจ็บตัว': {user_input}"
                response = model.generate_content(prompt)
                
                st.balloons() # เพิ่มเอฟเฟกต์ลูกโป่งตอนทำเสร็จ
                st.markdown("### ⚪ ผลลัพธ์พลังงาน:")
                st.info(response.text)
            except:
                st.error("ระบบขัดข้อง โปรดลองใหม่")
    else:
        st.warning("กรุณาใส่ข้อมูลก่อนครับ!")

st.markdown("---")
st.caption("🔵🔴⚪ SYNAPSE 6D HIGH-PERFORMANCE SYSTEM")
