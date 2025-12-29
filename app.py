import streamlit as st
import numpy as np
import torch
import os
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import torchaudio

# --- 1. ตั้งค่าหน้าตาแอปและโลโก้ ---
st.set_page_config(page_title="Hifi Music Studio", page_icon="🎙️", layout="wide")

# โลโก้แอป (คุณสามารถเปลี่ยนลิงก์รูปตรงนี้ได้)
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/4612/4612464.png" 

# --- 2. ฟังก์ชันโหลดโมเดล (รันในเครื่อง) ---
@st.cache_resource
def load_all_models():
    # ใช้รุ่น small เพื่อให้รันในเครื่องได้ลื่นๆ แต่เสียงยังใส
    model = MusicGen.get_pretrained('facebook/musicgen-small')
    return model

# --- 3. UI ส่วนหัว ---
st.image(LOGO_URL, width=100)
st.title("🎙️ AI Music & Vocal: สมจริงขั้นสุด")
st.markdown("### สโลแกน: **'อยู่นิ่งๆ ไม่เจ็บตัว'** (Local No-API System)")

# --- 4. ส่วนรับข้อมูล (Input) ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎹 ด้านดนตรี (Instrumental)")
        inst_prompt = st.text_area("อธิบายดนตรี:", "Acoustic guitar with soft violin and cinematic percussion, studio quality, 4k")
        
    with col2:
        st.subheader("🎤 ด้านเสียงร้อง (Vocal)")
        vocal_prompt = st.text_area("อธิบายเสียงร้อง:", "Male operatic voice, powerful, emotional, clear lyrics, studio recording")

    duration = st.slider("ความยาวเพลง (วินาที)", 5, 15, 8)

# --- 5. ระบบประมวลผล ---
if st.button("เริ่มรังสรรค์ผลงานสมจริง ✨"):
    model = load_all_models()
    
    with st.spinner("กำลังคำนวณคลื่นเสียงสมจริง... กรุณารอสักครู่ (ไม่ต้องเจ็บตัวครับ)"):
        # ตั้งค่าเวลา
        model.set_generation_params(duration=duration)
        
        # สร้างดนตรี (Instrumental)
        wav_inst = model.generate([inst_prompt + ", high-fidelity, mastered"])
        
        # สร้างเสียงร้อง (Vocal)
        wav_vocal = model.generate([vocal_prompt + ", clear human singing, expressive"])
        
        # ระบบ Mixer: รวมสอง Track เข้าด้วยกัน (Simple Sum & Normalize)
        mixed_wav = (wav_inst + wav_vocal) / 2
        
        # บันทึกไฟล์แยกและไฟล์รวม
        # กลยุทธ์ 'loudness' ช่วยให้เสียงใสและไม่แตก
        audio_write('instrumental', wav_inst[0].cpu(), model.sample_rate, strategy="loudness")
        audio_write('vocal', wav_vocal[0].cpu(), model.sample_rate, strategy="loudness")
        audio_write('final_mix', mixed_wav[0].cpu(), model.sample_rate, strategy="loudness")

        # --- 6. แสดงผลลัพธ์ ---
        st.divider()
        st.success("✅ สร้างเสร็จสมบูรณ์!")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1:
            st.write("🎹 ดนตรีประกอบ")
            st.audio("instrumental.wav")
        with res_col2:
            st.write("🎤 เสียงร้อง AI")
            st.audio("vocal.wav")
        with res_col3:
            st.write("🏆 **ไฟล์รวมสมจริง (Mix)**")
            st.audio("final_mix.wav")
            
            with open("final_mix.wav", "rb") as f:
                st.download_button("ดาวน์โหลดผลงาน", f, file_name="ai_masterpiece.wav")

st.info("💡 **Tips เพื่อความสมจริง:** การระบุคำว่า 'Studio recording', 'Acoustic', '4k audio' ในช่องกรอกข้อมูล จะช่วยให้ AI เลือกคลื่นเสียงที่ใสและคมชัดขึ้นครับ")
