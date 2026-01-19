import streamlit as st
import librosa
import numpy as np
import pyworld as pw
import io
import requests
import soundfile as sf

st.title("🎤 SYNAPSE Studio: รันระบบนับ 1 (ปรับตามความยาวเสียง)")

base_url = "https://raw.githubusercontent.com/leehunna789-boop/Synapse-6d2/main/"

uploaded_file = st.file_uploader("📤 อัปโหลดเสียงร้อง/พูด เนื้อเพลงของคุณ", type=['wav', 'mp3'])

if uploaded_file and st.button("🔥 เริ่มการเนรมิต (นับ 1 ของจริง)"):
    with st.spinner("⏳ กำลังจัดระเบียบเวลาและทำนอง..."):
        # 1. โหลดเสียงของคุณ
        y_user, sr = librosa.load(uploaded_file, sr=16000)
        y_user = y_user.astype(np.float64)
        
        # 2. โหลดแม่แบบจาก GitHub
        res_ref = requests.get(base_url + "rnb_vocal_ref.wav")
        y_ref, _ = librosa.load(io.BytesIO(res_ref.content), sr=16000)
        y_ref = y_ref.astype(np.float64)

        # 3. วิเคราะห์เสียง
        f0_u, t_u = pw.harvest(y_user, sr)
        sp_u = pw.cheaptrick(y_user, f0_u, t_u, sr)
        ap_u = pw.d4c(y_user, f0_u, t_u, sr)
        
        f0_ref, t_ref = pw.harvest(y_ref, sr)
        
        # --- [จุดสำคัญ] จัดการเรื่องความยาวเนื้อเพลง ---
        # บีบหรือยืดทำนองจากต้นฉบับให้เท่ากับเวลาที่ผู้ใช้ร้องจริง
        new_f0 = np.interp(np.linspace(0, t_ref[-1], len(t_u)), t_ref, f0_ref)
        
        # 4. สังเคราะห์เสียงใหม่
        y_tuned = pw.synthesize(new_f0, sp_u, ap_u, sr)
        
        # 5. รวมกับบีท
        res_beat = requests.get(base_url + "rnb_beat_full.wav")
        y_beat, _ = librosa.load(io.BytesIO(res_beat.content), sr=16000)
        
        min_len = min(len(y_tuned), len(y_beat))
        final_mix = y_tuned[:min_len] + (y_beat[:min_len] * 0.5)

        st.audio(final_mix, sample_rate=sr)
        st.success("✅ ประมวลผลสำเร็จ! นี่คือเสียงใหม่ที่ยาวตามเนื้อเพลงที่คุณร้องครับ")
