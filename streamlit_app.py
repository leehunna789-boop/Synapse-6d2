import streamlit as st
import librosa
import numpy as np
import soundfile as sf
import io
import os

# --- 1. การตั้งค่าหน้าตาแอป ---
st.set_page_config(page_title="SYNAPSE Tuner", layout="centered")
st.title("🔢 SYNAPSE Pure Math Tuner")
st.write("ระบบปรับจูนระดับเสียงด้วยสูตรลอการิทึม (เทียบกับไฟล์มาตรฐาน)")

# --- 2. ฟังก์ชันคำนวณคณิตศาสตร์ (จูนเสียง) ---
def tune_with_math(source_file, target_file):
    # โหลดไฟล์เสียง
    y_src, sr_src = librosa.load(source_file)
    y_ref, sr_ref = librosa.load(target_file)
    
    # ตรวจหาความถี่หลัก (f0)
    f0_src, _, _ = librosa.pyin(y_src, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    f0_ref, _, _ = librosa.pyin(y_ref, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    
    # หาค่าเฉลี่ย Hz
    avg_src = np.nanmean(f0_src)
    avg_ref = np.nanmean(f0_ref)
    
    if not np.isnan(avg_src) and not np.isnan(avg_ref):
        # สูตรคณิตศาสตร์: หาจำนวนครึ่งเสียง (Semitones) ที่ต้องขยับ
        shift_n = 12 * np.log2(avg_ref / avg_src)
        
        # ปรับ Pitch ด้วยค่าที่คำนวณได้
        y_tuned = librosa.effects.pitch_shift(y_src, sr=sr_src, n_steps=shift_n)
        
        # เขียนไฟล์ลง Memory
        buffer = io.BytesIO()
        sf.write(buffer, y_tuned, sr_src, format='WAV')
        return buffer.getvalue(), shift_n, avg_src, avg_ref
    return None, 0, 0, 0

# --- 3. ส่วนควบคุมการทำงาน ---

# เช็กไฟล์มาตรฐานใน GitHub
if os.path.exists("abcd.wav"):
    st.success("✅ ระบบพร้อมใช้งาน (พบไฟล์มาตรฐาน abcd.wav)")
    
    # ช่องอัปโหลดไฟล์เสียงเพี้ยน
    user_audio = st.file_uploader("อัปโหลดไฟล์เสียงที่ต้องการจูน (เช่น mymusic.wav)", type=['wav', 'mp3', 'm4a'])
    
    if user_audio:
        st.audio(user_audio, format='audio/wav')
        
        if st.button("🧮 เริ่มคำนวณและปรับเสียง"):
            with st.spinner("🧠 กำลังประมวลผลสูตรคณิตศาสตร์..."):
                output, n, f_src, f_ref = tune_with_math(user_audio, "abcd.wav")
                
                if output:
                    st.divider()
                    st.subheader("📊 ผลการคำนวณทางคณิตศาสตร์")
                    
                    # แสดงสูตรที่ใช้
                    st.latex(rf"\Delta n = 12 \times \log_2 \left( \frac{{f_{{ref}}}}{{f_{{src}}}} \right)")
                    st.write(f"ความถี่อ้างอิง ($f_{{ref}}$): **{f_ref:.2f} Hz**")
                    st.write(f"ความถี่เดิม ($f_{{src}}$): **{f_src:.2f} Hz**")
                    st.info(f"ต้องปรับแก้ทั้งหมด: **{n:.2f} Semitones**")
                    
                    st.subheader("🎧 เสียงที่ปรับจูนแล้ว")
                    st.audio(output, format='audio/wav')
                    st.download_button("📥 ดาวน์โหลดไฟล์", output, file_name="synapse_tuned.wav")
                else:
                    st.error("❌ ไม่สามารถคำนวณได้: อาจเป็นเพราะเสียงไม่ชัดเจนหรือไม่มีความถี่ที่ตรวจจับได้")
else:
    st.error("❌ ไม่พบไฟล์ abcd.wav ใน GitHub คลังไฟล์ของคุณ")
    st.info("กรุณาอัปโหลดไฟล์เสียงมาตรฐานโดยตั้งชื่อว่า abcd.wav ขึ้นไปที่ GitHub ก่อนครับ")
