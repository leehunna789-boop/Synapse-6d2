import streamlit as st
import google.generativeai as genai
import numpy as np
import soundfile as sf
import json
import re
import matplotlib.pyplot as plt
import matplotlib

# --- [ตั้งค่า] ---
matplotlib.use('Agg')
st.set_page_config(page_title="SYNAPSE: X-RAY", page_icon="🔍")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("⛔ ใส่ Key ก่อนครับ")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# --- [เครื่องยนต์สร้างเสียง] ---
def real_ai_engine(duration, fs, params):
    t = np.linspace(0, duration, int(fs * duration))
    # รับค่าจาก AI
    freq = params.get('frequency', 174)
    beat = params.get('binaural_beat', 6)
    
    # สร้างเสียง
    left = 0.5 * np.sin(2 * np.pi * freq * t)
    right = 0.5 * np.sin(2 * np.pi * (freq + beat) * t)
    
    return np.vstack((left, right)).T * 0.5, freq

# --- [หน้าจอ X-RAY] ---
st.title("🔍 SYNAPSE: X-Ray Mode")
st.caption("เปิดเผยการทำงานทุกขั้นตอน (จะได้รู้ว่าไม่ปลอม)")

user_input = st.text_input("พิมพ์ความรู้สึก (เพื่อดูสมอง AI ทำงาน):")

if st.button("START X-RAY"):
    if user_input:
        with st.status("กำลังผ่าตัดระบบดูไส้ใน...", expanded=True):
            
            # 1. ขั้นตอนส่งคำสั่ง
            st.write("---")
            st.info("1. ส่งคำสั่งไป Google (Prompt):")
            st.code(f'Analyze: "{user_input}" -> Return JSON Physics')
            
            # 2. ขั้นตอนรับความคิด AI
            prompt = f"""
            Analyze emotion: "{user_input}"
            Return ONLY a JSON object:
            {{
                "frequency": (float 100-600),
                "binaural_beat": (float 1-10),
                "message": (Thai short quote)
            }}
            """
            response = model.generate_content(prompt)
            
            # 3. โชว์ของดิบ (Raw Output) ** นี่คือสิ่งที่พี่ไม่เคยเห็น **
            st.write("---")
            st.info("2. สิ่งที่ AI ตอบกลับมา (Raw Data):")
            st.text(response.text) # <--- โชว์ข้อความดิบๆ จาก AI เลย
            
            # 4. แปลงเป็นตัวเลข
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                ai_data = json.loads(match.group())
                
                st.write("---")
                st.info(f"3. แปลงเป็นตัวเลขสำหรับเครื่องจักร:")
                # โชว์ให้เห็นจะๆ ว่าเลขนี้มาจาก AI
                col1, col2 = st.columns(2)
                col1.metric("Frequency (Hz)", ai_data['frequency'])
                col2.metric("Binaural Beat (Hz)", ai_data['binaural_beat'])
                
                # 5. สร้างเสียงจากเลขข้างบน
                y, f = real_ai_engine(60, 44100, ai_data)
                sf.write("xray.wav", y, 44100)
                
                st.write("---")
                st.success("4. ผลลัพธ์สุดท้าย (เสียง + ข้อความ):")
                st.audio("xray.wav")
                st.write(f"💬 {ai_data['message']}")
            else:
                st.error("AI ตอบมาผิดรูปแบบ")
