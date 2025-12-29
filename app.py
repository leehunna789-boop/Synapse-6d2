import streamlit as st
import numpy as np
import librosa
import os
import google.generativeai as genai

# --- 1. การตั้งค่าหน้าจอและดีไซน์ (OLED / 60-30-10 Rule) ---
st.set_page_config(page_title="SYNAPSE 6D PRO", layout="wide")

st.markdown("""
    <style>
    /* พื้นหลังดำสนิทเพื่อสีที่คมชัดแบบ OLED */
    .stApp { background-color: #000000; font-family: 'Kanit', sans-serif; }
    
    .neon-red-logo { 
        color: #FF0000; 
        text-shadow: 0 0 25px #FF0000, 0 0 45px rgba(255,0,0,0.6); 
        font-size: 70px; 
        text-align: center; 
        font-weight: 900; 
        letter-spacing: 5px;
    }
    
    .slogan-text { 
        color: #00FF00; 
        text-shadow: 0 0 10px #00FF00; 
        text-align: center; 
        font-size: 20px; 
        margin-top: -20px;
        font-weight: 300;
    }

    .luxury-card {
        background: linear-gradient(145deg, rgba(30, 30, 30, 0.9), rgba(10, 10, 10, 0.9));
        border: 2px solid #00F2FE;
        border-radius: 20px;
        padding: 35px;
        margin-bottom: 25px;
        box-shadow: 0px 10px 30px rgba(0, 242, 254, 0.2);
    }
    
    h1, h2, h3, p, label { color: #FFFFFF !important; }
    
    .stButton>button {
        background: #FF0000;
        color: white;
        border-radius: 50px;
        padding: 15px 40px;
        border: none;
        box-shadow: 0 0 20px rgba(255,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. การเชื่อมต่อ AI Core ---
ai_active = False
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        ai_active = True
        st.sidebar.success("✅ Gemini AI Core: Active")
    else:
        st.sidebar.warning("⚠️ API Key not found. Using Standalone mode.")
except Exception:
    st.sidebar.error("❌ AI Connection Error")

# --- 3. ระบบประมวลผลเสียง (Universal Audio Engine) ---
def synape_audio_mixer(vocal_file, bass_file):
    if not os.path.exists(vocal_file) or not os.path.exists(bass_file):
        return None, "System: Audio files not found on server."
    
    try:
        # ใช้ Librosa เพื่อรองรับไฟล์ .wav ทุกรูปแบบ (แก้ปัญหา b'\x00' error)
        vocal, sr_v = librosa.load(vocal_file, sr=44100)
        bass, sr_b = librosa.load(bass_file, sr=44100)
        
        # ปรับความยาวให้เท่ากัน (Rhythm Alignment)
        min_len = min(len(vocal), len(bass))
        vocal = vocal[:min_len]
        bass = bass[:min_len]
        
        # ผสมเสียง (Vocal 1.0 + Bass 0.8)
        mixed = (vocal * 1.0) + (bass * 0.8)
        
        # Mastering: Normalize ป้องกันเสียงแตก
        mixed = mixed / np.max(np.abs(mixed))
        
        return (mixed * 32767).astype(np.int16), 44100, None
    except Exception as e:
        return None, None, str(e)

# --- 4. หน้าหลัก DASHBOARD ---
st.markdown('<p class="neon-red-logo">SYNAPSE</p>', unsafe_allow_html=True)
st.markdown('<p class="slogan-text">อยู่นิ่งๆ ไม่เจ็บตัว | SOUND & AI THERAPY</p>', unsafe_allow_html=True)

st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
user_prompt = st.text_area("บอกความในใจของคุณ ให้ AI ช่วยนำทางบทเพลง...", placeholder="วันนี้รู้สึกเหงาๆ อยากฟังแร็พแบบลึกๆ...")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 ACTIVATE SYNAPSE 6D"):
    with st.spinner("กำลังจูนความถี่และวิเคราะห์สัญญาณประสาท..."):
        # 1. ผสมเสียงดนตรีจริง
        mixed_audio, sr, error = synape_audio_mixer("my_vocal.wav", "rap_bass.wav")
        
        if error:
            st.error(f"Error: {error}")
        elif mixed_audio is not None:
            # 2. เรียก AI แต่งเนื้อเพลง (ถ้ามี API)
            lyrics = "ยินดีต้อนรับสู่โหมด Standalone บทเพลงนี้สร้างจากตัวตนของคุณ"
            if ai_active and user_prompt:
                prompt = f"แต่งเนื้อเพลงแร็พ/R&B จากข้อความ: {user_prompt}"
                response = model.generate_content(prompt)
                lyrics = response.text
            
            # 3. แสดงผล Layout
            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown(f"""
                <div class="luxury-card">
                    <h3>🎵 บทเพลงของคุณ</h3>
                    <p style="white-space: pre-wrap;">{lyrics}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_r:
                st.audio(mixed_audio, sample_rate=sr)
                st.line_chart(mixed_audio[:20000]) # แสดง Waveform คมชัด
                st.success("✅ Synchronization Complete")

st.sidebar.markdown("---")
st.sidebar.write("MODE: **PRO 6.0**")
st.sidebar.write("สโลแกน: **อยู่นิ่งๆ ไม่เจ็บตัว**")
