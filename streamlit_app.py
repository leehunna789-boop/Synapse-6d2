import streamlit as st
import google.generativeai as genai
import numpy as np
import soundfile as sf
import json
import re
import matplotlib.pyplot as plt
import matplotlib

# --- [ส่วนที่ 1: เตรียมระบบ (Setup)] ---
matplotlib.use('Agg') # ตั้งค่ากราฟไม่ให้ตีกับ Server
st.set_page_config(page_title="SYNAPSE: FINAL REAL", page_icon="🧬")

# เช็คกุญแจ (ถ้าไม่มี Key โค้ดนี้เป็นแค่เศษกระดาษ)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⛔ CRITICAL: ไม่พบ API Key ใน Settings")
    st.stop()

# เชื่อมต่อกับสมอง AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- [ส่วนที่ 2: สร้างเครื่องยนต์ (Define Engine)] ---
# นี่คือคำสั่ง def ที่คุณถามหา (สร้างเครื่องรอไว้)
def real_ai_engine(duration, fs, params):
    t = np.linspace(0, duration, int(fs * duration))
    
    # [จุดตรวจสอบความจริง]: รับค่าจาก params เท่านั้น (ไม่มีการกำหนดเลขเอง)
    freq = params.get('frequency', 174)      # <--- รับความถี่จาก AI
    beat = params.get('binaural_beat', 6)    # <--- รับจังหวะจาก AI
    speed = params.get('breath_speed', 0.2)  # <--- รับความเร็วหายใจจาก AI
    
    # สร้างคลื่นเสียง (Physics Logic)
    left = 0.5 * np.sin(2 * np.pi * freq * t)
    right = 0.5 * np.sin(2 * np.pi * (freq + beat) * t)
    
    # Effect การหายใจ (Modulation)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * speed * t)
    
    # รวมเสียงซ้ายขวา
    audio = np.vstack((left*lfo, right*lfo)).T * 0.5
    return audio, freq, lfo

# --- [ส่วนที่ 3: หน้าจอสั่งงาน (User Interface)] ---
st.title("🧬 SYNAPSE: AI-Core Integration")
st.caption("Status: Ready to Link Logic & Sound")

user_input = st.text_input("ระบุความรู้สึก (Input Signal):")

# --- [ส่วนที่ 4: สวิตช์เริ่มทำงาน (Execution Trigger)] ---
# นี่คือคำสั่ง if st.button ที่สั่งให้เริ่มระบบ
if st.button("START PROCESS"):
    if not user_input:
        st.warning("กรุณาป้อนข้อมูลก่อนสตาร์ทเครื่อง")
    else:
        with st.status("⚙️ Executing Neural Protocol...", expanded=True):
            
            # A. สั่งงาน AI (Prompting)
            st.write("1. Sending signal to Gemini...")
            prompt = f"""
            Analyze emotion: "{user_input}"
            Return a JSON object ONLY with these parameters:
            {{
                "frequency": (float 100-600, e.g. 174 for pain, 528 for love),
                "binaural_beat": (float 1-10),
                "breath_speed": (float 0.1-1.0),
                "message": (Thai quote ending with "อยู่นิ่งๆ ไม่เจ็บตัว")
            }}
            """
            
            try:
                # B. รับผลและแปลภาษา (Listening & Parsing)
                response = model.generate_content(prompt)
                
                # นี่คือคำสั่ง json.loads ที่ใช้แกะกล่องของขวัญ
                match = re.search(r'\{.*\}', response.text, re.DOTALL)
                ai_data = json.loads(match.group()) 
                
                st.success("2. AI Data Decoded:")
                st.json(ai_data) # <--- โชว์หลักฐานว่า AI ส่งเลขอะไรมา
                
                # C. [จุดเชื่อมต่อสำคัญ] (Connection Point)
                # เอา "น้ำมัน" (ai_data) เติมเข้า "เครื่องยนต์" (real_ai_engine)
                st.write("3. Synthesizing Audio Waves...")
                y, val_freq, val_lfo = real_ai_engine(60, 44100, ai_data)
                
                # บันทึกไฟล์
                sf.write("synapse_real.wav", y, 44100)
                
                # D. แสดงผล (Output)
                st.divider()
                
                # วาดกราฟพิสูจน์
                fig, ax = plt.subplots(2, 1, figsize=(8, 5), facecolor='#0e1117')
                ax[0].plot(val_lfo[:500], color='#00ff00') # กราฟการหายใจ
                ax[0].set_title("AI-Controlled Breathing LFO", color='white')
                ax[0].set_facecolor('#0e1117')
                
                ax[1].axhline(y=val_freq, color='#ff00ff', linewidth=3) # กราฟความถี่
                ax[1].set_title(f"Target Frequency: {val_freq} Hz", color='white')
                ax[1].set_facecolor('#0e1117')
                st.pyplot(fig)
                
                # เล่นเสียงและโชว์ข้อความ
                st.audio("synapse_real.wav")
                st.info(f"💬 {ai_data['message']}")
                
            except Exception as e:
                st.error(f"❌ System Error: {e}")
