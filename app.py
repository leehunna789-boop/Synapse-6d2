import numpy as np
import streamlit as st
import google.generativeai as genai
import json, io, os

# --- 1. SETUP & CONNECTION ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # ใช้ชื่อรุ่นมาตรฐานที่เสถียรที่สุด
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ ไม่พบ API Key ใน Secrets")
    st.stop()

# --- 2. UI DESIGN ---
st.set_page_config(page_title="SYNAPSE Matrix", layout="centered")

# แสดงโลโก้ (ถ้ามีไฟล์ logo.jpg ใน GitHub)
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)

st.markdown("<h1 style='text-align: center; color: #00d2ff;'>SYNAPSE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>GLOBAL ENERGY MATRIX</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)

user_text = st.text_area("ระบุสภาวะจิตใจของคุณตอนนี้...", placeholder="เช่น วันนี้รู้สึกดีจัง", height=120)

if st.button("🚀 ACTIVATE MATRIX MAPPING"):
    if user_text:
        try:
            with st.status("🔮 AI กำลังวิเคราะห์สภาวะของคุณ...", expanded=True) as status:
                prompt = f"Analyze: '{user_text}'. Return ONLY JSON format: {{'v': 0.5, 'a': 0.5, 'weather': 'Sunny'}}"
                response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                
                data = json.loads(response.text)
                v = data.get('v', 0.5)
                
                status.update(label="✅ Matrix Synced สำเร็จ!", state="complete")

            # แสดงผลลัพธ์
            st.success(f"ระดับพลังงานปัจจุบันของคุณคือ {v*100:.0f}%")
            st.balloons()
            
        except Exception as e:
            st.error(f"ระบบขัดข้อง: {e}")
    else:
        st.warning("กรุณาป้อนข้อความก่อนครับ")
