import streamlit as st
import librosa
import numpy as np
import parselmouth
import io

st.title("🎙 เครื่องวัดค่าเสียงแม่นยำสูง (Vocal Master Engine)")

uploaded_file = st.file_uploader("อัปโหลดไฟล์เสียงเพื่อวัดค่า", type=['wav', 'mp3'])

if uploaded_file is not None:
    # อ่านไฟล์เสียง
    file_bytes = uploaded_file.read()
    snd = parselmouth.Sound(file_bytes)
    
    # แปลงเป็น numpy สำหรับ librosa
    y, sr = librosa.load(io.BytesIO(file_bytes), sr=None)

    # 1. การสั่น (Vibrato) - หา Standard Deviation ของ Pitch (Hz)
    pitch = snd.to_pitch()
    f0 = pitch.selected_array['frequency']
    v_pitches = f0[f0 > 0] # กรองเฉพาะตอนที่มีเสียง
    vibrato_val = np.std(v_pitches) if len(v_pitches) > 0 else 0

    # 2. การเอื้อน (Pitch Transition) - วัดความต่างระหว่างโน้ตต่อโน้ต
    transition_val = np.mean(np.abs(np.diff(v_pitches))) if len(v_pitches) > 1 else 0

    # 3. น้ำหนักเสียง (Timbre) - วัดค่าความใส (Spectral Centroid)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    timbre_val = np.mean(centroid)

    # 4. ความดัง-เบา (Dynamics) - วัดค่า RMS (พลังงานเสียง)
    rms = librosa.feature.rms(y=y)
    dynamics_val = np.mean(rms) * 100 # คูณ 100 ให้เห็นตัวเลขชัดขึ้น

    # 5. จังหวะคำ (Phoneme Timing) - วัดจำนวนการขยับของเสียงต่อวินาที
    onsets = librosa.onset.onset_detect(y=y, sr=sr)
    duration = librosa.get_duration(y=y, sr=sr)
    timing_val = len(onsets) / duration if duration > 0 else 0

    # 6. เสียงแหลม (Sibilance) - วัด Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y)
    sibilance_val = np.mean(zcr)

    # 7. คุมความเงียบ (Silence Gate) - วัด Noise Floor (ค่าพลังงานต่ำสุด)
    silence_val = np.min(rms) if len(rms) > 0 else 0

    # --- แสดงผลหน้าจอแบบตัวเลขเน้นๆ ---
    st.markdown("### 📊 ผลการวัดค่าเพื่อกำหนดแนวเพลง")
    
    cols = st.columns(2)
    with cols[0]:
        st.metric("1. Vibrato (สั่น)", f"{vibrato_val:.2f} Hz")
        st.metric("2. Transition (เอื้อน)", f"{transition_val:.4f}")
        st.metric("3. Timbre (เนื้อเสียง)", f"{timbre_val:.2f}")
        st.metric("4. Dynamics (น้ำหนัก)", f"{dynamics_val:.4f}")
    with cols[1]:
        st.metric("5. Timing (จังหวะ)", f"{timing_val:.2f} onset/sec")
        st.metric("6. Sibilance (เสียงแหลม)", f"{sibilance_val:.4f}")
        st.metric("7. Silence Gate (ความเงียบ)", f"{silence_val:.6f}")

    # ปุ่มสำหรับดูข้อมูลแบบดิบ
    if st.button("ดูรายงานสรุปสำหรับก๊อปปี้"):
        report = {
            "vibrato": vibrato_val,
            "transition": transition_val,
            "timbre": timbre_val,
            "dynamics": dynamics_val,
            "timing": timing_val,
            "sibilance": sibilance_val,
            "silence": silence_val
        }
        st.json(report)
