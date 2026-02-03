import streamlit as st
import numpy as np
import requests
import json

# 1. วางส่วนหัว (Imports) ไว้บนสุด
st.set_page_config(page_title="Identity Sound")

# 2. วางฟังก์ชันช่วยสร้างเสียงไว้ตรงกลาง
def generate_audio(params):
    sr = 44100
    t = np.linspace(0, 2, int(sr * 2), False)
    freq = params.get('rbf1_freq', 440)
    # สร้างคลื่นเสียงแบบง่าย
    audio = 0.5 * np.sin(2 * np.pi * freq * t)
    return (audio * 32767).astype(np.int16).tobytes()

# 3. ส่วน UI หลัก
st.title("🎵 Identity Sound Creator")
key = st.text_input("Gemini API Key:", type="password")
query = st.text_area("อธิบายตัวตนของคุณ:")

if st.button("สร้างเสียง"):
    if key and query:
        # --- จุดที่เชื่อมต่อกับ AI ---
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + key
        prompt = "Analyze: " + query + ". Output JSON: {explanation: string (Thai), rbf_parameters: {gain, rbf1_freq}}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        
        res = requests.post(api_url, json=payload)
        data = res.json()
        
        # ดึงคำตอบมาแสดง
        text_resp = data['candidates'][0]['content']['parts'][0]['text']
        result_json = json.loads(text_resp)
        
        st.write(result_json['explanation'])
        
        # สร้างเสียงและแสดงตัวเล่นเพลง
        sound = generate_audio(result_json['rbf_parameters'])
        st.audio(sound, format="audio/wav", sample_rate=44100)
    else:
        st.error("กรุณากรอกข้อมูลให้ครบ")
