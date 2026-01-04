import streamlit as st
import google.generativeai as genai
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import matplotlib

# --- [ส่วนที่ 1: ตั้งค่าระบบ] ---
matplotlib.use('Agg')
st.set_page_config(page_title="SYNAPSE", page_icon="🌐")

# วางโลโก้
try:
    st.image("logo.jpg", width=200)
except:
    pass # ถ้าไม่มีโลโก้ก็ข้ามไป ไม่ต้องแจ้งเตือน

# ตั้งค่า API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- [ส่วนที่ 2: ตั้งค่าโมเดล Gemini] ---
instruction = (
    "คุณคือนักแต่งเพลง แนว Industrial/Dark Minimalist "
    "สโลแกน: 'อยู่นิ่งๆ ไม่เจ็บตัว' "
    "กฎ: แต่งเนื้อเพลงสั้นๆ 4 บรรทัด พร้อมคอร์ด และข้อความฮีลใจตอนท้าย"
)
model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=instruction)

# --- [ส่วนที่ 3: Engine เสียงใหม่ (ใช้ Numpy ล้วน ไม่ต้องใช้ pyworld)] ---
def synapse_lite_engine(duration, fs, mood_valence):
    # สร้างแกนเวลา
    t = np.linspace(0, duration, int(fs * duration))
    
    # กำหนดความถี่พื้นฐาน (Base Frequency) ตามอารมณ์
    # อารมณ์ดี (High Valence) = เสียงสูงขึ้นนิดหน่อย / เศร้า = เสียงทุ้มลึก
    base_freq = 110 if mood_valence < 0.5 else 174 # Hz (Solfeggio Frequencies)
    
    # สร้างคลื่นเสียง (Sine Wave) ผสมกับ (Binaural Beat)
    # หูซ้าย
    left_channel = 0.5 * np.sin(2 * np.pi * base_freq * t)
    # หูขวา (เพี้ยนไปนิดหน่อยเพื่อให้สมองสร้างคลื่นบำบัด)
    beat_freq = 6 # Theta waves (ผ่อนคลาย)
    right_channel = 0.5 * np.sin(2 * np.pi * (base_freq + beat_freq) * t)
    
    # รวมเป็น Stereo
    audio_stereo = np.vstack((left_channel, right_channel)).T
    
    # สร้างข้อมูลหลอกๆ เพื่อไปวาดกราฟ (Mock Data)
    f0_mock = np.ones_like(t) * base_freq + np.random.normal(0, 2, len(t))
    sp_mock = np.abs(np.fft.rfft(left_channel[:1024])) # สุ่มวิเคราะห์ช่วงสั้นๆ
    
    return audio_stereo, f0_mock, sp_mock

# --- [ส่วนที่ 4: UI] ---
st.title("🌐 SYNAPSE: Lite Core")
st.caption("Mode: Frequency Therapy (No Vocoder)")

user_note = st.text_input("ระบุสิ่งที่กวนใจคุณ...", placeholder="EXECUTE YOUR PAIN HERE...")

if st.button("EXECUTE & HEAL"):
    if user_note:
        with st.spinner('Accessing Neural Network...'):
            # 1. Gemini แต่งเพลง
            try:
                response = model.generate_content(user_note)
                st.subheader("🎵 Text Output")
                st.write(response.text)
            except:
                st.error("API Key มีปัญหา หรือเน็ตหลุด")

            # 2. สร้างเสียงบำบัด
            fs = 44100
            duration = 10 # วินาที
            mood = 0.3 if "เจ็บ" in user_note or "เศร้า" in user_note else 0.8
            
            y, f0, sp = synapse_lite_engine(duration, fs, mood)
            
            # 3. บันทึกและเล่น
            output_path = "synapse_signal.wav"
            sf.write(output_path, y, fs)
            
            # 4. แสดงผล
            st.audio(output_path)
            
            # กราฟ
            fig, ax = plt.subplots(2, 1, figsize=(10, 6), facecolor='#0e1117')
            
            # กราฟบน (Pitch)
            ax[0].plot(f0[:1000], color='#00ff00', linewidth=1) # สีเขียว Terminal
            ax[0].set_facecolor('#0e1117')
            ax[0].set_title("Frequency Stability", color='white')
            ax[0].tick_params(colors='white')
            
            # กราฟล่าง (Spectrum)
            ax[1].plot(sp, color='#ff00ff', linewidth=1) # สีม่วง Neon
            ax[1].set_facecolor('#0e1117')
            ax[1].set_title("Energy Spectrum", color='white')
            ax[1].tick_params(colors='white')
            
            st.pyplot(fig)
            st.success("Process Complete. Stay Still.")
            
    else:
        st.warning("Input required.")
