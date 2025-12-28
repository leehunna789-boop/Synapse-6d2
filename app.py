import numpy as np
import streamlit as st
import google.generativeai as genai
import json, io, os, time, requests, geocoder
import pandas as pd
from scipy.io import wavfile

# --- 1. CONFIGURATION & AI CORE ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # ใช้ชื่อรุ่นที่สั้นและถูกต้องเพื่อแก้ Error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ ไม่พบ GEMINI_API_KEY ใน Secrets")
    st.stop()

# --- 2. DATA STRUCTURE ---
MATRIX_V1 = {"JOY": {"F0": 0.8, "Vib": 0.9}, "SAD": {"F0": 0.3, "Vib": 0.2}}
MATRIX_V2 = {
    "JOY": {"SAT": 0.9, "LIGHT": 0.8},
    "SAD": {"SAT": 0.2, "LIGHT": 0.3}
}

# --- 3. FUNCTIONS ---
def get_live_environment():
    try:
        g = geocoder.ip('me')
        lat, lon = g.latlng
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        res = requests.get(url).json()
        return {"weather": "Rainy" if res['current_weather']['weathercode'] >= 51 else "Sunny"}
    except:
        return {"weather": "Sunny"}

# --- 4. UI ---
st.title("💠 SYNAPSE CORE V3.1")
st.markdown("*\"อยู่นิ่งๆ ไม่เจ็บตัว\"*")

user_input = st.text_area("ป้อนสภาวะภายในของคุณ...", placeholder="เช่น เบื่อ หรือ เซ็ง")

if st.button("🚀 ACTIVATE MATRIX SYNC"):
    if user_input:
        try:
            env = get_live_environment()
            prompt = f"Analyze: '{user_input}'. Return ONLY JSON: {{'v': 0.0-1.0}}"
            res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            v = json.loads(res.text).get('v', 0.5)
            st.success(f"✅ ซิงค์สำเร็จ! ค่า Valence: {v}")
            st.balloons()
        except Exception as e:
            st.error(f"ระบบขัดข้อง: {e}")
