import streamlit as st
import numpy as np
import time
import os

# --- 1. ตั้งค่าหน้าจอและสไตล์ (Perfect UI) ---
st.set_page_config(page_title="SYNAPSE 6D ENERGY PRO", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stButton>button { background: linear-gradient(45deg, #FF4B2B, #FF416C); color: white; border-radius: 20px; font-weight: bold; width: 100%; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ระบบคำนวณพลังงาน (จากโค้ดที่คุณส่งมา) ---
MATRIX_V1 = {"JOY": {"F0": 0.8, "Vibrato": 0.9}, "SAD": {"F0": 0.3, "Vibrato": 0.2}}
MATRIX_V2 = {"JOY": {"SAT": 0.9, "LIGHT": 0.8, "CONTRAST": 0.8}, "SAD": {"SAT": 0.2, "LIGHT": 0.3, "CONTRAST": 0.4}}

def lerp(low, high, factor): return low + (high - low) * factor

def synthesize_music_pro(v):
    f0 = lerp(MATRIX_V1["SAD"]["F0"], MATRIX_V1["JOY"]["F0"], v)
    vibrato = lerp(MATRIX_V1["SAD"]["Vibrato"], MATRIX_V1["JOY"]["Vibrato"], v)
    t = np.linspace(0, 5, 44100 * 5)
    wave = 0.5 * np.sin(2 * np.pi * (440 * f0) * t + (vibrato * np.sin(2 * np.pi * 5 * t)))
    envelope = np.ones_like(t)
    fade_len = 44100 // 2
    envelope[:fade_len] = np.linspace(0, 1, fade_len)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    audio = (wave * envelope * 32767).astype(np.int16)
    return audio

# --- 3. แสดงผลโลโก้และสโลแกน ---
logo_file = "logo.jpg" 
if os.path.exists(logo_file):
    st.image(logo_file, use_container_width=True) # แสดงโลโก้ที่อัปโหลดไว้

st.markdown("<h3 style='text-align: center;'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</h3>", unsafe_allow_html=True)

# --- 4. ส่วนการใช้งาน ---
st.write("---")
user_input = st.text_area("วันนี้คุณรู้สึกอย่างไร?", placeholder="เช่น วันนี้เหนื่อยจังแต่ก็ยังยิ้มได้")

if st.button("🚀 เริ่มการบำบัด (Fully Automated)"):
    if user_input:
        with st.spinner("ระบบกำลังคำนวณ Matrix และซิงค์พลังงาน..."):
            # จำลองการวิเคราะห์จากระบบ AI
            time.sleep(1.5)
            mood_value = 0.75 # ค่าจำลองความสุข
            
            # สร้างเสียงบำบัดจริงจากคณิตศาสตร์
            audio_data = synthesize_music_pro(mood_value)
            
            # คำนวณค่า Visual (SAT, LIGHT, CONTRAST)
            sat = lerp(MATRIX_V2["SAD"]["SAT"], MATRIX_V2["JOY"]["SAT"], mood_value)
            light = lerp(MATRIX_V2["SAD"]["LIGHT"], MATRIX_V2["JOY"]["LIGHT"], mood_value)
            
            st.balloons()
            st.subheader(f"🔊 พลังงานบำบัดที่ส่งให้คุณ (Intensity: {mood_value})")
            st.audio(audio_data, format='audio/wav', sample_rate=44100)
            
            c1, c2 = st.columns(2)
            c1.metric("ความสว่างพลังงาน", f"{light:.2f}")
            c2.metric("ความอิ่มสีของออร่า", f"{sat:.2f}")
            
            st.success(f"สโลแกนของคุณ: 'อยู่นิ่งๆ ไม่เจ็บตัว' - ระบบบำบัดให้เรียบร้อยครับ")
    else:
        st.warning("กรุณาพิมพ์ข้อความเพื่อวิเคราะห์พลังงาน")

# --- 5. ส่วนท้าย ---
st.markdown("---")
st.caption("🔵🔴⚪ SYNAPSE 6D HIGH-PERFORMANCE SYSTEM")
