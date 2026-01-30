import streamlit as st
import numpy as np
import pandas as pd
import time

# --- 1. CONFIG & STYLE (ดึงธีมจาก UI Android ที่คุณส่งมา) ---
st.set_page_config(layout="wide", page_title="S.S.S Music - Ultimate AI")
st.markdown("""
    <style>
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    .stButton>button { background-color: #FF0000; color: white; width: 100%; height: 3em; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #1A1A1A; color: white; }
    h1 { color: #FF0000; text-align: center; }
    .slogan { color: #FFD700; text-align: center; font-size: 1.2em; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC: 12 DIMENSIONS & EMOTION (ดึงจากตาราง 12 มิติ และ Matrix V1/V2) ---
def get_vocal_parameters(v):
    # ใช้ Linear Interpolation (Lerp) ตามที่คุณถาม เพื่อความสมูท
    def lerp(low, high, factor): return low + (high - low) * factor
    
    return {
        "Vibrato_Hz": lerp(4.5, 6.0, v),
        "Spectral_Tilt": lerp(-6, -12, v), # ยิ่งเศร้าเสียงยิ่งนุ่ม (Slope ชัน)
        "HNR": lerp(15, 25, v),            # ลมหายใจ
        "F0_Base": lerp(220, 440, v),      # ระดับเสียง (Hz)
        "RT60": lerp(1.2, 2.5, v)          # ความก้องของห้อง
    }

# --- 3. ENGINE: PRO SYNTHESIS (ดึงจากโค้ด Ultimate AI และ SVS) ---
def synthesize_healing_voice(params, duration=3, sr=44100):
    t = np.linspace(0, duration, sr * duration)
    f0 = params["F0_Base"]
    vib_hz = params["Vibrato_Hz"]
    
    # 432Hz Healing Frequency Logic
    # ผสม Fundamental + Harmonics (ลดการบาดหูตามที่คุณตั้งใจ)
    audio = 0.5 * np.sin(2 * np.pi * f0 * t + (0.5 * np.sin(2 * np.pi * vib_hz * t)))
    overtone = 0.2 * np.sin(2 * np.pi * (f0 * 2) * t) 
    combined = audio + overtone
    
    # Apply Envelope (Fade in/out) ป้องกันเสียงคลิก
    envelope = np.ones_like(t)
    fade = 44100 // 2
    envelope[:fade] = np.linspace(0, 1, fade)
    envelope[-fade:] = np.linspace(1, 0, fade)
    
    # Mastering (Limiter)
    final_audio = np.clip(combined * envelope, -0.9, 0.9)
    return final_audio

# --- 4. UI: FRONTEND (ถอดแบบจาก Android XML ที่คุณส่งมา) ---
st.write("<h1>S.S.S Music</h1>", unsafe_allow_html=True)
st.write("<p class='slogan'>\"อยู่นิ่งๆ ไม่เจ็บตัว\"</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.image("https://img5.pic.in.th/file/secure-sv1/logo_world.png", caption="AI Album Cover", width=300) # จำลอง Logo
    user_note = st.text_input("ใจความสั้นๆ ที่จะให้ AI ขยี้...", placeholder="เช่น วันนี้เหนื่อยจัง...")
    btn_gen = st.button("ขยี้ใจความ (GENERATE)")

with col2:
    st.subheader("📊 AI Control Matrix (12 มิติ)")
    # จำลองค่าจาก Gemini (Logic: ถ้ามีคำว่าเหนื่อย/เศร้า ให้ Valence ต่ำ)
    v_val = 0.3 if "เหนื่อย" in user_note or "เศร้า" in user_note else 0.7
    a_val = 0.4
    
    params = get_vocal_parameters(v_val)
    
    # แสดงค่าพารามิเตอร์ที่เปลี่ยนไปตาม "ใจความ"
    df_params = pd.DataFrame({
        "มิติความสมจริง": params.keys(),
        "ค่าที่ AI ปรับแต่ง": params.values()
    })
    st.table(df_params)

# --- 5. EXECUTION (เมื่อกดปุ่ม ขยี้ใจความ) ---
if btn_gen:
    with st.spinner("🤖 AI Gemini กำลังวิเคราะห์อารมณ์และส่งต่อให้ RBF Engine..."):
        time.sleep(1.5) # จำลองการประมวลผล
        
        # รันเครื่องยนต์เสียง
        audio_data = synthesize_healing_voice(params)
        
        st.success("✅ สังเคราะห์เสียงบำบัดเสร็จสมบูรณ์!")
        
        # แสดงผล Visual ตาม V2.0 (IP Asset 100M THB ของคุณ)
        st.subheader("🎨 Visual Feedback (V2.0 Logic)")
        sat = 0.2 if v_val < 0.5 else 0.8
        st.info(f"ระบบปรับค่า Saturation ไปที่: {sat} | แสงสว่าง: {params['RT60']/3:.2f}")
        
        # เล่นเสียง
        st.audio(audio_data, format="audio/wav", sample_rate=44100)
        
        # ปุ่มเสริมจาก UI Android
        c_save, c_share, c_turbo = st.columns(3)
        c_save.button("SAVE")
        c_share.button("SHARE")
        c_turbo.button("TURBO (High-Res)")

st.markdown("---")
st.caption("ระบบรันบนสถาปัตยกรรม: Input -> Gemini -> RBF -> Mastering")
