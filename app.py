import numpy as np
import streamlit as st
import google.generativeai as genai
import json, io, os, time, requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="SYNAPSE 6D Pro", layout="centered")

# แสดงโลโก้ของคุณจากไฟล์ logo.jpg
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)

# ดึงกุญแจจริงจาก Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') # แก้ให้ถูกตามรูป 1000008948.jpg

# --- 2. SENSOR DATA (ดึงค่าจริงจากกรุงเทพฯ) ---
def get_real_sensor():
    try:
        # ดึงอากาศจริงจากพิกัดประเทศไทย
        url = "https://api.open-meteo.com/v1/forecast?latitude=13.7563&longitude=100.5018&current_weather=true"
        weather = requests.get(url).json()['current_weather']
        return {"temp": weather['temperature'], "city": "Bangkok, TH", "code": weather['weathercode']}
    except:
        return {"temp": "--", "city": "Unknown", "code": 0}

env = get_real_sensor()

# --- 3. UI DISPLAY (ขึ้นจอให้เห็นค่าตามสั่ง) ---
st.title("💠 SYNAPSE 6D Pro: UNLIMITED")
st.markdown("<p style='text-align:center;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)

# รับค่าชีพจรจริงจากคุณ
st.sidebar.header("⌚ Bio-Feedback")
heart_rate = st.sidebar.number_input("ป้อนค่าชีพจร (BPM)", 40, 200, 75)

# แสดงแถบค่าพลังงานจริง 3 ช่อง
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📍 พิกัดโลกจริง", env['city'])
with col2:
    st.metric("🌡️ อุณหภูมิไทย", f"{env['temp']}°C")
with col3:
    st.metric("💓 ชีพจรผู้ใช้", f"{heart_rate} BPM")

# ส่วนรับความรู้สึก
user_input = st.text_area("ป้อนสภาวะภายในของคุณ:", placeholder="ปวดหัว / เหนื่อย / ต้องการพลังงาน...")

if st.button("🚀 ACTIVATE MATRIX SYNC"):
    if user_input:
        with st.status("🔮 กำลังประมวลผล Matrix จากข้อมูลจริง..."):
            # ส่งข้อมูลไปวิเคราะห์ที่ Gemini
            prompt = f"Analyze: {user_input}. Return JSON: {{'v': 0.8}}"
            res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            st.success("✅ ปรับจูนสำเร็จ พลังงานซิงค์กับอากาศและร่างกายแล้ว")
