import streamlit as st
import google.generativeai as genai
from slack_sdk import WebClient
import numpy as np

# --- 1. ตั้งค่าพื้นฐานและการดึงกุญแจ (Secrets) ---
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    SLACK_TOKEN = st.secrets["SLACK_TOKEN"]
    
    # เริ่มต้นระบบ AI และ Slack
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    slack_client = WebClient(token=SLACK_TOKEN)
except Exception as e:
    st.error("❌ ไม่พบ API Key ในระบบ Secrets กรุณาตั้งชื่อให้ถูกต้อง")
    st.stop()

# --- 2. หน้าตาแอป (UI) ---
st.set_page_config(page_title="Synapse Sound & Visual", layout="wide")

# ใส่ logo จากไฟล์ที่คุณอัปโหลดไว้ใน GitHub
st.image("logo.jpg", width=300) 
st.title("🎵 RBF AI Music Composer")
st.markdown("### สโลแกน: *อยู่นิ่งๆ ไม่เจ็บตัว*")

# แถบด้านข้างแสดงสถานะ
st.sidebar.header("⚙️ ระบบบำบัดเสียงและภาพ")
st.sidebar.info("สถานะ: เชื่อมต่อ API เรียบร้อย ✅")

# ส่วนรับข้อมูล
topic = st.text_input("ระบุหัวข้อเพลงที่ต้องการแต่ง", "Sound & Visual Therapy")

if st.button("🚀 เริ่มแต่งเพลงและส่งไปที่ Slack", type="primary"):
    with st.spinner("AI กำลังประมวลผล..."):
        try:
            # ใช้ Gemini แต่งเพลง
            prompt = f"แต่งเนื้อเพลงและคอร์ดสำหรับ: {topic}"
            response = model.generate_content(prompt)
            lyrics = response.text
            
            # แสดงเนื้อเพลง
            st.subheader("📝 ผลงานจาก AI")
            st.write(lyrics)
            
            # จำลองเสียง (Simulated Audio)
            sr = 44100
            audio_wave = np.random.uniform(-0.1, 0.1, sr * 3)
            st.audio(audio_wave, format='audio/wav', sample_rate=sr)
            
            # ส่งเข้า Slack (ปลดล็อกระดับ 4 ของคุณ)
            slack_client.chat_postMessage(
                channel="general", 
                text=f"🎶 *แต่งเพลงใหม่เสร็จแล้ว!* \n*หัวข้อ:* {topic}\n\n{lyrics}"
            )
            st.success("✅ ส่งเข้า Slack เรียบร้อย! (Stay Still & Heal)")

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")

# ส่วนแสดง Log (Engine Log)
with st.expander("🛠️ รายละเอียดการทำงาน"):
    st.write("- ดึงข้อมูลจาก GitHub: app.py, requirements.txt, logo.jpg")
    st.write("- ประมวลผลผ่านโมเดล: gemini-1.5-flash")
    st.write("- การส่งข้อมูล: Slack API (Level 4 Rate Limit)")
