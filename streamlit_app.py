import streamlit as st
import librosa
import numpy as np
import pyworld as pw
import io
import requests
import soundfile as sf

st.title("🎤 SYNAPSE Studio: Full Song Processor (3 Minutes)")

base_url = "https://raw.githubusercontent.com/leehunna789-boop/Synapse-6d2/main/"

# ส่วนอัปโหลดไฟล์ 3 นาทีของคุณ
uploaded_file = st.file_uploader("📤 อัปโหลดไฟล์เสียงร้องฝรั่ง (3 นาที)", type=['wav', 'mp3'])

if uploaded_file and st.button("🔥 เริ่มการเนรมิตเพลงเต็ม"):
    # แสดงแถบความคืบหน้าเพราะไฟล์ยาว
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("⏳ ขั้นตอนที่ 1: กำลังโหลดและวิเคราะห์ไฟล์เสียง...")
        # โหลดเสียงร้อง 3 นาที (ใช้ sr=16000 เพื่อความเร็ว)
        y_user, sr = librosa.load(uploaded_file, sr=16000)
        y_user = y_user.astype(np.float64)
        progress_bar.progress(30)

        status_text.text("⏳ ขั้นตอนที่ 2: กำลังดึงแม่แบบทำนองจาก GitHub...")
        res_ref = requests.get(base_url + "rnb_vocal_ref.wav")
        y_ref, _ = librosa.load(io.BytesIO(res_ref.content), sr=sr)
        y_ref = y_ref.astype(np.float64)
        progress_bar.progress(50)

        status_text.text("⏳ ขั้นตอนที่ 3: คณิตศาสตร์ pyworld กำลังทำงาน (ขั้นตอนนี้จะนานหน่อย)...")
        # ใช้ Harvest วิเคราะห์ระดับเสียง
        f0_u, t_u = pw.harvest(y_user, sr)
        sp_u = pw.cheaptrick(y_user, f0_u, t_u, sr)
        ap_u = pw.d4c(y_user, f0_u, t_u, sr)
        
        f0_ref, t_ref = pw.harvest(y_ref, sr)
        
        # ปรับทำนองให้ยาวเท่ากับไฟล์ 3 นาทีของคุณ
        new_f0 = np.interp(np.linspace(0, t_ref[-1], len(t_u)), t_ref, f0_ref)
        
        # สังเคราะห์เสียงใหม่
        y_tuned = pw.synthesize(new_f0, sp_u, ap_u, sr)
        progress_bar.progress(80)

        status_text.text("⏳ ขั้นตอนสุดท้าย: กำลังมิกซ์เข้ากับบีท...")
        res_beat = requests.get(base_url + "rnb_beat_full.wav")
        y_beat, _ = librosa.load(io.BytesIO(res_beat.content), sr=sr)
        
        # มิกซ์เสียง
        min_len = min(len(y_tuned), len(y_beat))
        final_mix = y_tuned[:min_len] + (y_beat[:min_len] * 0.5)
        
        progress_bar.progress(100)
        status_text.success("✅ เนรมิตเพลง 3 นาทีสำเร็จแล้ว!")

        st.audio(final_mix, sample_rate=sr)
        
    except Exception as e:
        st.error(f"⚠️ เกิดข้อผิดพลาด: {e}")
        st.info("ถ้าแอปค้าง ให้ลองใช้ไฟล์ที่สั้นลง (เช่น 1 นาที) เพื่อทดสอบก่อนครับ")
