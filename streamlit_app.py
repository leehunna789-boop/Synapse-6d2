import streamlit as st

# --- ตั้งค่าหน้าตาแอปให้เหมือน Android XML ของลูกพี่ ---
st.set_page_config(page_title="SYNAPSE 6D Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Matrix Display Header */
    .matrix-display {
        display: flex;
        justify-content: space-between;
        background-color: #1A0000;
        padding: 10px;
        border-bottom: 2px solid #330000;
    }
    .v1 { color: #FFD700; font-weight: bold; font-size: 10px; }
    .v2 { color: #00F2FE; font-weight: bold; font-size: 10px; }

    /* Neon Ring จาก XML 280dp */
    .neon-ring {
        width: 280px;
        height: 280px;
        margin: 40px auto;
        border: 6px solid #FF0000;
        border-radius: 50%;
        box-shadow: 0 0 30px #FF0000, inset 0 0 20px #FF0000;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle, #330000 0%, #050505 100%);
    }
    
    /* ปรับแต่งเครื่องเล่นเพลงของระบบให้เข้ากับธีมดำ */
    audio { filter: invert(100%) hue-rotate(180deg) brightness(1.5); width: 100%; }
    </style>

    <div class="matrix-display">
        <div class="v1">V1: VOCAL ACTIVE</div>
        <div class="v2">V2: VISUAL 6D ON</div>
    </div>

    <div class="neon-ring">
        <h1 style="color: white; font-size: 50px; text-shadow: 2px 2px #000;">S.S.S</h1>
    </div>

    <div style="text-align: center;">
        <h2 style="margin-bottom: 0;">MUSIC 6D PLAYER</h2>
        <p style="color: #FF0000; font-weight: bold;">"อยู่นิ่งๆ ไม่เจ็บตัว"</p>
    </div>
""", unsafe_allow_html=True)

# --- ส่วนควบคุมเครื่องเล่นเพลง ---
st.markdown("---")
st.subheader("🎵 NOW PLAYING")

# ลูกพี่สามารถเปลี่ยนลิงก์เพลงตรงนี้เป็นไฟล์ .mp3 ของลูกพี่ได้เลย
track_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
st.audio(track_url)

st.info("📊 Status: ระบบ 6D พร้อมขยี้ความรู้สึก | กด Play เพื่อเริ่ม")
