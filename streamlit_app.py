import streamlit as st
import google.generativeai as genai
import pyworld as pw  # ใช้ pw สำหรับ pyworld
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import matplotlib # นำเข้าเพื่อตั้งค่า Backend

# ตั้งค่า Matplotlib ให้รันบน Server ได้ (ใช้ชื่อ matplotlib ตรงๆ)
matplotlib.use('Agg') 

# 1. ตั้งค่าความปลอดภัยเรียกใช้กุญแจจาก Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# กำหนด System Instruction ตามบทบาทนักแต่งเพลงของคุณ
instruction = (
    "คุณคือนักแต่งเพลงมืออาชีพ สโลแกนคือ 'อยู่นิ่งๆ ไม่เจ็บตัว' "
    "กฎ: ต้องระบุคอร์ดเหนือเนื้อเพลง และวิเคราะห์คำศัพท์ตอนท้ายเสมอ"
)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', 
    system_instruction=instruction
)

# 2. ฟังก์ชันหลักสำหรับวิเคราะห์และสังเคราะห์เสียงร้อง (Matrix V1)
def synapse_vocal_engine(input_audio, fs, valence):
    # วิเคราะห์เสียงต้นแบบ (Analysis)
    # ใช้ High-level API ตามที่คุณระบุ
    f0, sp, ap = pw.wav2world(input_audio, fs)
    
    # ขยี้อารมณ์ด้วย Matrix V1 (Pitch Control)
    # ปรับ f0 ตามค่าความสุข/เศร้า (Valence)
    # ตัวอย่าง: ถ้าเศร้า f0 จะต่ำลง
    modified_f0 = f0 * (0.8 + (valence * 0.4))
    
    # สังเคราะห์กลับเป็นเสียงใหม่ (Synthesis)
    y = pw.synthesize(modified_f0, sp, ap, fs)
    return y, modified_f0, sp

# 3. ส่วนการแสดงผลบนหน้าจอ (UI)
st.set_page_config(page_title="SYNAPSE", page_icon="🌐")
st.title("🌐 SYNAPSE: Sound & Visual Therapy")
st.caption("Slogan: อยู่นิ่งๆ ไม่เจ็บตัว (Stay Still & Heal)") #

# ช่องรับ Input
user_note = st.text_input("ใจความสั้นๆ ที่จะให้ AI ขยี้...", placeholder="เช่น ความเหงาในเมืองใหญ่")

if st.button("GENERATE & HEAL"):
    with st.spinner('AI กำลังขยี้ใจความและสังเคราะห์เสียงบำบัด...'):
        # --- ส่วนของ Gemini ---
        response = model.generate_content(user_note)
        st.subheader("🎵 Lyrics & Chords")
        st.write(response.text) #
        
        # --- ส่วนของ PyWorld (จำลองเสียงต้นแบบ) ---
        # ในการใช้งานจริงควรใช้ไฟล์เสียงร้องที่คุณเตรียมไว้
        fs = 44100
        t = np.linspace(0, 2, fs * 2)
        x = np.sin(2 * np.pi * 440 * t).astype(np.float64) # Dummy input
        
        # สมมติค่า Valence จากเนื้อหา (0.0 - 1.0)
        mood_valence = 0.3 if "เหงา" in user_note or "เศร้า" in user_note else 0.7
        
        # รันเครื่องยนต์เสียง
        y, f0_new, sp_new = synapse_vocal_engine(x, fs, mood_valence)
        
        # บันทึกไฟล์เสียง
        output_path = "syntinsefs.wav"
        sf.write(output_path, y, fs)
        
        # --- ส่วนการแสดงผลกราฟ (Visual Therapy) ---
        st.subheader("📊 Visual Matrix Analysis")
        fig, ax = plt.subplots(2, 1, figsize=(10, 6))
        
        ax[0].plot(f0_new, color='#FF0000') # สีแดงตามธีมคุณ
        ax[0].set_title('Pitch Contour (f0)')
        
        ax[1].imshow(np.log(sp_new).T, aspect='auto', origin='lower', cmap='magma')
        ax[1].set_title('Spectral Envelope (Voice Identity)')
        
        st.pyplot(fig) # แสดงผลผ่าน Agg mode
        
        # เล่นเสียง
        st.audio(output_path)
        st.success("บำบัดสำเร็จ! ข้อมูลถูกบันทึกลง Story List แล้ว")
