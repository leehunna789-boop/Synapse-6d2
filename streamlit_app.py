import streamlit as st
import google.generativeai as genai
import pyworld as pw
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import matplotlib

# --- [ส่วนที่ 1: ตั้งค่าระบบ] ---
matplotlib.use('Agg') 

# ต้องวาง st.set_page_config ไว้บนสุดของส่วนแสดงผล
st.set_page_config(page_title="SYNAPSE", page_icon="🌐")

# วางโลโก้ (ตรวจสอบว่ามีไฟล์ logo.jpg ในโฟลเดอร์เดียวกับโค้ด)
try:
    st.image("logo.jpg", width=200)
except:
    st.warning("ไม่พบไฟล์ logo.jpg กรุณาตรวจสอบตำแหน่งไฟล์")

# ตั้งค่า API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("กรุณาใส่ API Key ใน Secrets")

# --- [ส่วนที่ 2: ตั้งค่าโมเดล Gemini] ---
instruction = (
    "คุณคือนักแต่งเพลงมืออาชีพ สโลแกนคือ 'อยู่นิ่งๆ ไม่เจ็บตัว' "
    "กฎ: ต้องระบุคอร์ดเหนือเนื้อเพลง และวิเคราะห์คำศัพท์ตอนท้ายเสมอ"
)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=instruction
) # <--- ปิดวงเล็บให้ถูกต้องตรงนี้

# --- [ส่วนที่ 3: ฟังก์ชันการประมวลผลเสียง (Synapse Engine)] ---
def synapse_vocal_engine(input_audio, fs, valence):
    x = input_audio.astype(np.float64)
    # Analysis
    f0, sp, ap = pw.wav2world(x, fs)
    # Pitch Control (มิติของอารมณ์)
    modified_f0 = f0 * (0.8 + (valence * 0.4))
    # Synthesis
    y = pw.synthesize(modified_f0, sp, ap, fs)
    return y, modified_f0, sp

# --- [ส่วนที่ 4: ส่วนแสดงผลหน้าจอ UI] ---
st.title("🌐 SYNAPSE: Sound & Visual Therapy")
st.caption("Slogan: อยู่นิ่งๆ ไม่เจ็บตัว (Stay Still & Heal)")

user_note = st.text_input("ใจความสั้นๆ ที่จะให้ AI ขยี้...", placeholder="เช่น ความเหงาในเมืองใหญ่")

if st.button("GENERATE & HEAL"):
    if user_note:
        with st.spinner('กำลังประมวลผล...'):
            # 1. ให้ Gemini แต่งเพลง
            response = model.generate_content(user_note)
            st.subheader("🎵 Lyrics & Chords")
            st.write(response.text)

            # 2. สร้างเสียงจำลอง (Simulation)
            fs = 44100
            t = np.linspace(0, 2, fs * 2)
            x = 0.5 * np.sin(2 * np.pi * 440 * t) # เสียง Sine wave พื้นฐาน
            
            # วิเคราะห์อารมณ์เบื้องต้น
            mood_valence = 0.3 if "เหงา" in user_note or "เศร้า" in user_note else 0.7
            
            # 3. รัน Engine เสียง
            y, f0_new, sp_new = synapse_vocal_engine(x, fs, mood_valence)
            
            # 4. บันทึกและแสดงผล
            output_path = "synapse_output.wav"
            sf.write(output_path, y, fs)
            
            # วาดกราฟ Visual Therapy
            fig, ax = plt.subplots(2, 1, figsize=(10, 6))
            ax[0].plot(f0_new, color='red')
            ax[0].set_title("Pitch Dimension")
            ax[1].imshow(np.log(sp_new).T, aspect='auto', origin='lower', cmap='magma')
            ax[1].set_title("Spectral Dimension")
            st.pyplot(fig)

            st.audio(output_path)
            st.success("บำบัดสำเร็จ! อยู่นิ่งๆ และฟังเสียงนี้นะครับ")
    else:
        st.warning("กรุณาพิมพ์ข้อความก่อนกดปุ่ม")
