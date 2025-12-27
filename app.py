import streamlit as st
import google.generativeai as genai
import numpy as np
import json
import time

# --- 1. ตั้งค่าดีไซน์ตามโลโก้ของคุณ (ม่วง-ดำ-เขียวมินต์) ---
st.set_page_config(page_title="SYNAPSE 6D Pro", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; } 
    h1, h2, h3 { color: #B266FF !important; text-shadow: 2px 2px 4px #000000; text-align: center; }
    .stMetric { background-color: #1E1E1E; border-radius: 10px; padding: 15px; border: 1px solid #B266FF; }
    .stButton>button { 
        background-color: #00CC99; 
        color: white; border-radius: 25px; width: 100%; font-weight: bold; height: 50px;
        box-shadow: 0px 4px 15px rgba(0, 204, 153, 0.3);
    }
    .stTextArea textarea { background-color: #1E1E1E; color: white; border: 1px solid #B266FF; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ตั้งค่าระบบ AI (ใส่ API Key ให้เรียบร้อยแล้ว) ---
# ผมใส่ Key เดิมที่คุณเคยใช้ไว้ให้เลยครับ จะได้ไม่ต้องหาใหม่
API_KEY = "AIzaSyBiKFHClySIV_UmeMznANnhyBoD78CYUrg"
genai.configure(api_key=API_KEY)

def get_ai_vibe(text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"วิเคราะห์อารมณ์จากข้อความ: '{text}' และตอบเป็น JSON เท่านั้น: {{'v': 0.8, 'rap': 'เนื้อเพลงแร็พ R&B สั้นๆ 1 ประโยค'}}"
        response = model.generate_content(prompt)
        # ทำความสะอาดข้อมูล JSON
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_res)
    except:
        # Safe Mode: ถ้าติดต่อ AI ไม่ได้ ให้ใช้ค่านี้แทน (อยู่นิ่งๆ ไม่เจ็บตัว)
        return {"v": 0.6, "rap": "ปล่อยใจไปกับจังหวะ R&B อยู่นิ่งๆ พลังงานจะดีเอง"}

# --- 3. ระบบสร้างเสียง Melodic R&B ---
def create_rb_sound(v):
    sr = 44100
    t = np.linspace(0, 5, sr * 5)
    # สร้างจังหวะ Kick นุ่มๆ แบบ R&B
    kick = np.sin(2 * np.pi * 55 * t) * np.exp(-7 * (t % 1.0))
    # สร้างเสียงคอร์ด Synth ละมุนๆ 432Hz
    freq = 432 * (1 + (v - 0.5))
    chord = 0.3 * np.sin(2 * np.pi * freq * t) + 0.1 * np.sin(2 * np.pi * freq * 1.2 * t)
    audio = (kick * 0.4) + (chord * 0.5)
    return (np.clip(audio, -0.9, 0.9) * 32767).astype(np.int16)

# --- 4. หน้าจอใช้งาน (UI) ---
# แสดงโลโก้ SYNAPSE 6D
try:
    st.image("1000008780.jpg", use_container_width=True)
except:
    st.title("💎 SYNAPSE : 6D ENERGY PRO")

st.write("### สโลแกน: 'อยู่นิ่งๆ ไม่เจ็บตัว'")

user_input = st.text_area("บอกความรู้สึกของคุณวันนี้ให้ระบบรับรู้:", placeholder="เช่น เหนื่อย ล้า หรือต้องการพลังงาน...")

if st.button("🚀 ACTIVATE ENERGY (เริ่มการบำบัด)"):
    if user_input:
        with st.spinner("ระบบกำลังปรับจูนคลื่นความถี่ R&B และแร็พ..."):
            vibe_data = get_ai_vibe(user_input)
            audio_bytes = create_rb_sound(vibe_data['v'])
            time.sleep(1.5) 
            
            st.subheader(f"🎤 Message: {vibe_data['rap']}")
            
            c1, c2 = st.columns(2)
            c1.metric("ความสว่างเซลล์", f"{vibe_data['v']*100:.0f}%")
            c2.metric("สถานะพลังงาน", "STABLE")
            
            st.audio(audio_bytes, format='audio/wav', sample_rate=44100)
            st.success("ปรับจูนพลังงานเรียบร้อย ยินดีด้วยครับ")
    else:
        st.error("กรุณากรอกความรู้สึกก่อนกดปุ่มครับ")
