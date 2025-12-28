import numpy as np
import streamlit as st
import google.generativeai as genai
import json, io, os, time, requests, geocoder
import pandas as pd
from scipy.io import wavfile

# --- 1. CONFIGURATION & AI CORE ---
# ดึงกุญแจ API จากหน้า Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # ใช้ชื่อรุ่นที่ถูกต้องเพื่อแก้ปัญหา Error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ ไม่พบ GEMINI_API_KEY ในหน้า Secrets")
    st.stop()

# --- 2. IP ASSET MATRIX (V1.0 & V2.0) ---
MATRIX_V1 = {"JOY": {"f0": 0.8, "vib": 0.9}, "SAD": {"f0": 0.3, "vib": 0.2}}
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8, "CON": 0.8, "DOF": 0.3, "TEX": 0.7, "FOC": 0.9},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CON": 0.4, "DOF": 0.8, "TEX": 0.8, "FOC": 0.3}
}

# --- 3. UI/UX DESIGN ---
st.set_page_config(page_title="SYNAPSE CORE", layout="centered")
st.markdown("<style>.stApp { background-color: #000428; color: white; }</style>", unsafe_allow_html=True)

# แสดงโลโก้
if os.path.exists("1000008875.jpg"):
    st.image("1000008875.jpg", use_container_width=True)

st.title("💠 SYNAPSE CORE V3.1")
st.markdown("*\"อยู่นิ่งๆ ไม่เจ็บตัว - ระบบจัดการทุกอย่างด้วยข้อมูลจริง\"*")

user_input = st.text_area("ป้อนสภาวะภายในของคุณ...", placeholder="เบื่อ / เหนื่อย / ต้องการพลังงาน...")

if st.button("🚀 ACTIVATE MATRIX SYNC"):
    if user_input:
        with st.status("🔮 กำลังซิงค์ข้อมูลจริงและ AI Matrix..."):
            try:
                # AI Analysis
                prompt = f"Analyze: '{user_input}'. Return ONLY JSON: {{'v': 0.0-1.0, 'a': 0.0-1.0}}"
                res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                data = json.loads(res.text)
                
                v = data.get('v', 0.5)
                st.subheader(f"📊 Emotional Matrix (Valence: {v*100:.1f}%)")
                st.balloons()
                st.success("✅ ปรับจูนพลังงานเรียบร้อยด้วยกุญแจจริงของคุณ")
            except Exception as e:
                st.error(f"ระบบขัดข้อง: {e}")
    else:
        st.error("กรุณากรอกความรู้สึกก่อนครับ")
