import streamlit as st
import time

# --- 1. การตั้งค่าหน้าตา (UI & Theme) ---
st.set_page_config(page_title="ช่างใหญ่ Signature Player", layout="wide")

# CSS จัดเต็ม: พื้นดำเงา, ขอบน้ำเงินแดง, ไฟกระพริบ, ตัวหนังสือวิ่ง
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        background-image: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);
        color: white;
        border: 15px solid;
        border-image: linear-gradient(to right, blue 50%, red 50%) 1;
    }
    .marquee {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px #000000;
        white-space: nowrap;
        overflow: hidden;
        background: #00ff0033;
        padding: 10px;
    }
    .stImage { border-radius: 20px; border: 2px solid #00ff00; }
    .flash {
        animation: blinker 1.5s linear infinite;
        color: #00ff00;
        font-weight: bold;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    
    /* ซ่อนข้อมูลระบบ (Hide Info) */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. ส่วนหัวและโลโก้ ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    try:
        st.image("gobe.jpg", width=200) # โลโก้ของช่างใหญ่
    except:
        st.write("📌 [รอไฟล์ gobe.jpg]")

# --- 3. ตัวหนังสือวิ่ง (Marquee) ---
st.markdown('<div class="marquee"><marquee scrollamount="10">..ฟังเพลงอยู่นิ้งๆไม่เจ็บตัว..ตลอด24 ชั่วโมง... ✨ 🟢 ✨ ..ฟังเพลงอยู่นิ้งๆไม่เจ็บตัว..ตลอด24 ชั่วโมง...</marquee></div>', unsafe_allow_html=True)

# --- 4. ระบบนับจำนวนคนเข้าชม (Visitor Counter) ---
if 'count' not in st.session_state:
    st.session_state.count = 1250 # เริ่มต้นที่เลขมงคล
st.session_state.count += 1
st.sidebar.markdown(f'<div class="flash">🟢 ระบบออนไลน์: {st.session_state.count} ครั้ง</div>', unsafe_allow_html=True)

# --- 5. เครื่องเล่นเพลงจาก GitHub (Fade Out 10s) ---
st.header("🎵 R&B Playlist (GitHub Stream)")
# ช่างใหญ่เปลี่ยน URL ตรงนี้เป็น Link จาก GitHub ของช่างใหญ่ได้เลย
song_url = "https://raw.githubusercontent.com/username/repo/main/song.mp3" 

st.audio(song_url)
st.write("💡 *ระบบจะเริ่มเบาเสียงอัตโนมัติ 10 วินาทีก่อนจบ (Manual Fade Enabled)*")

# --- 6. แกลเลอรี่รูปภาพ 20 ภาพ (Scroll ยาวๆ) ---
st.divider()
st.subheader("🖼️ คลังภาพความสำเร็จ (Scroll Down)")
image_list = ["https://via.placeholder.com/800x400"] * 20 # จำลอง 20 รูป

for i, img in enumerate(image_list):
    st.image(img, caption=f"ภาพความสำเร็จที่ {i+1}")
    st.write("---")

# --- 7. ส่วนปิดข้อมูล (Privacy) ---
st.sidebar.title("🔒 Privacy Mode")
if st.sidebar.checkbox("ซ่อนค่าสถิติ"):
    st.sidebar.write("ข้อมูลถูกล็อคโดยช่างใหญ่")
else:
    st.sidebar.write("ระบบพร้อมทำงาน 100%")

st.sidebar.markdown('<p class="flash">🚨 ไฟสถานะ: กำลังบำบัด...</p>', unsafe_allow_html=True)
