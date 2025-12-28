Import numpy as np
import streamlit as st
import google.generativeai as genai
import json, io, os, time, requests
import pandas as pd
from scipy.io import wavfile

# --- 1. CONFIGURATION & AI CORE ---
# ดึงกุญแจ API จากระบบ Secrets ของ Streamlit (วิธีที่ปลอดภัยที่สุด)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # ใช้ชื่อรุ่น 'gemini-1.5-flash' เพื่อป้องกัน Error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ ไม่พบ GEMINI_API_KEY ใน Streamlit Secrets")
    st.info("กรุณาไปที่หน้า Settings > Secrets ใน Streamlit Cloud แล้วใส่ API Key")
    st.stop()

# --- 2. DATA STRUCTURE (MATRIX) ---
# โครงสร้างข้อมูลที่คุณออกแบบไว้
MATRIX_V1 = {"JOY": {"F0": 0.8, "Vib": 0.2}}
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3}
}

# --- 3. FUNCTIONS ---
def get_live_environment():
    """ฟังก์ชันสำหรับดึงข้อมูลสภาพแวดล้อม (ตัวอย่าง)"""
    try:
        # คุณสามารถเพิ่มโค้ดดึงสภาพอากาศหรือพิกัดจริงตรงนี้ได้
        return {"status": "online", "sync_time": time.ctime()}
    except Exception as e:
        return {"error": str(e)}

# --- 4. USER INTERFACE (UI) ---
st.title("🚀 SYNAPSE-6D2 MATRIX SYNC")
st.write("สถานะระบบ: เชื่อมต่อกับ Gemini 1.5 Flash แล้ว")

user_input = st.text_area("ป้อนสภาวะภายในของคุณ...", placeholder="เช่น เบื่อ, มีความสุข")

if st.button("🚀 ACTIVATE MATRIX SYNC"):
    if user_input:
        with st.spinner("🔮 กำลังประมวลผลข้อมูลจริงและ AI Matrix..."):
            try:
                # ส่งคำสั่งไปที่ AI
                prompt = f"วิเคราะห์สภาวะ '{user_input}' และจับคู่กับค่าใน Matrix: {MATRIX_V2}"
                response = model.generate_content(prompt)
                
                st.subheader("ผลการวิเคราะห์")
                st.write(response.text)
                
                # แสดงข้อมูล Environment
                env_data = get_live_environment()
                st.json(env_data)
                
            except Exception as e:
                st.error(f"ระบบขัดข้อง: {str(e)}")
    else:
        st.warning("กรุณาพิมพ์ข้อความก่อนกดปุ่มครับ")

# --- 5. FOOTER ---
st.divider()
st.caption("สโลแกน: อยู่นิ่งๆ ไม่เจ็บตัว")
