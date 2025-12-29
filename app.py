import streamlit as st
import numpy as np
import pandas as pd
import os
import io
from scipy.io import wavfile

# --- 1. SET THEME & LAYOUT ---
st.set_page_config(page_title="SYNAPSE 6D PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; font-family: 'Kanit', sans-serif; }
    .neon-red-logo { color: #FF0000; text-shadow: 0 0 25px #FF0000; font-size: 65px; text-align: center; font-weight: 900; }
    .slogan-text { color: #00FF00; text-shadow: 0 0 10px #00FF00; text-align: center; font-size: 20px; margin-top: -15px; }
    .luxury-card {
        background: rgba(20, 20, 20, 0.9);
        border: 2px solid #00F2FE;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0px 8px 25px rgba(0, 242, 254, 0.3);
    }
    h1, h2, h3, p, label { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGO ---
st.markdown('<p class="neon-red-logo">SYNAPSE</p>', unsafe_allow_html=True)
st.markdown('<p class="slogan-text">SOUND & VISUAL THERAPY | อยู่นิ่งๆ ไม่เจ็บตัว</p>', unsafe_allow_html=True)

# --- 3. MOCK AI & DATA ENGINE ---
class SynapseEngine:
    def __init__(self):
        self.fs = 44100
        # คลังข้อมูลสำหรับจำลอง AI (Mock Database)
        self.genre_logic = {
            "Rap": {"valence": 0.3, "harmonics": "sawtooth", "chords": "Am, F, E"},
            "R&B": {"valence": 0.8, "harmonics": "sine", "chords": "Cmaj7, Am7, G7"}
        }

    def simulate_ai_analysis(self, user_text, bpm):
        """จำลองการวิเคราะห์ของ AI โดยไม่ต้องใช้ API"""
        genre = "R&B" if "เหงา" in user_text or "รัก" in user_text or bpm < 85 else "Rap"
        config = self.genre_logic[genre]
        
        return {
            "song_title": f"Digital Resonance: {genre} Mode",
            "genre": genre,
            "lyrics": f"ในจังหวะชีพจรที่ {bpm} BPM...\nความรู้สึกของคุณบอกว่า '{user_text}'\nSYNAPSE กำลังเปลี่ยนมันเป็นทำนอง...",
            "mood_score": config["valence"],
            "visual_query": "neon city" if genre == "Rap" else "calm ocean sunset"
        }

    def synthesize_6d_audio(self, bpm, genre_name):
        """สร้างเสียงเครื่องดนตรีจริง (Sample-based Logic)"""
        duration = 8.0
        t = np.linspace(0, duration, int(self.fs * duration), endpoint=False)
        base_freq = 432 + (bpm - 70) * 0.2
        
        # เลือกลักษณะเสียงตามแนวเพลง
        if genre_name == "Rap":
            # เสียงดิบ แน่น มี Overtones แบบ Sawtooth
            wave = 0.6 * np.sin(2 * np.pi * base_freq * t) + 0.2 * (2 * (t * base_freq - np.floor(0.5 + t * base_freq)))
        else:
            # เสียงนุ่มนวลแบบ Electric Piano (Sine Harmonics)
            wave = 0.5 * np.sin(2 * np.pi * base_freq * t) + 0.2 * np.sin(2 * np.pi * base_freq * 2 * t)
            
        # ใส่จังหวะการเต้น (Pulse) ตาม BPM
        pulse = 0.5 * (1 + np.sin(2 * np.pi * (bpm/60) * t))
        final_wave = wave * pulse
        
        # Mastering (Envelope & Limit)
        fade = int(self.fs * 0.5)
        env = np.ones_like(t)
        env[:fade] = np.linspace(0, 1, fade)
        env[-fade:] = np.linspace(1, 0, fade)
        
        return (np.clip(final_wave * env, -0.8, 0.8) * 32767).astype(np.int16)

# --- 4. MAIN DASHBOARD ---
engine = SynapseEngine()

st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
st.subheader("📝 ความรู้สึกของคุณในตอนนี้")
user_input = st.text_area("พิมพ์เล่าเรื่องราวหรืออารมณ์ของคุณที่นี่...", placeholder="เช่น วันนี้รู้สึกดีมาก หรือ กำลังเศร้า...")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 ACTIVATE SYNAPSE 6D", type="primary"):
    if user_input:
        # จำลองการอ่านค่า Sensor
        bpm = np.random.randint(65, 110)
        
        with st.spinner("ประมวลผลสัญญาณประสาท..."):
            # 1. AI Analysis (Mock)
            ai_data = engine.simulate_ai_analysis(user_input, bpm)
            
            # 2. Audio Synthesis
            audio_raw = engine.synthesize_6d_audio(bpm, ai_data['genre'])
            
            # 3. Display Results
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="luxury-card">
                    <h3>🎵 {ai_data['song_title']}</h3>
                    <p><b>สไตล์:</b> {ai_data['genre']}</p>
                    <p><b>ชีพจรขณะนี้:</b> {bpm} BPM</p>
                    <hr>
                    <p style="white-space: pre-wrap;">{ai_data['lyrics']}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                # แสดงภาพจำลอง (ใช้ URL จาก Unsplash)
                img_url = f"https://source.unsplash.com/featured/?{ai_data['visual_query']}"
                st.image("https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=1000", caption="VISUAL RESONANCE")
                
                st.audio(audio_raw, sample_rate=44100)
                
                st.metric("EMOTIONAL BALANCE", f"{int(ai_data['mood_score']*100)}%")
                st.progress(ai_data['mood_score'])
    else:
        st.warning("กรุณาพิมพ์ความรู้สึกของคุณก่อนเริ่มกระบวนการ")

st.sidebar.markdown("---")
st.sidebar.write("MODE: **OFFLINE STANDALONE**")
st.sidebar.write("สโลแกน: **อยู่นิ่งๆ ไม่เจ็บตัว**")
