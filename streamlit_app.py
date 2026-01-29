import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from streamlit_player import st_player 

# --- [ตั้งค่าหน้าเว็บ] ---
st.set_page_config(page_title="สถานีอยู่นิ่งๆ ไม่เจ็บตัว", page_icon="📻", layout="wide")

# --- [CSS ตกแต่ง - คงเดิมตามที่คุณชอบ] ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 10px; }
    .stButton>button { 
        width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; border: none;
        transition: 0.3s;
    }
    .song-card {
        background-color: #1e2129; padding: 20px; border-radius: 15px; 
        margin-bottom: 15px; border-left: 6px solid #FF4B4B;
    }
    .song-title { font-size: 1.2rem; font-weight: bold; color: #ffffff; }
    .user-name { color: #FF4B4B; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# --- [เชื่อมต่อ Firebase] ---
if not firebase_admin._apps:
    try:
        # ใช้ชื่อ sooksun1 ตามที่ตั้งใน Secrets
        key_dict = st.secrets["sooksun1"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"ระบบฐานข้อมูลขัดข้อง: {e}")

db = firestore.client()

# --- [Layout หน้าเว็บ] ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3658/3658959.png", width=100) # โลโก้ชั่วคราว
    st.title("About Station")
    st.write("ยินดีต้อนรับสู่สถานีที่เงียบที่สุด")

col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.title("📻 สถานี 'อยู่นิ่งๆ ไม่เจ็บตัว' 📀")
    # ใส่ลิงก์เพลง YouTube ของคุณที่นี่
    st_player("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 

with col_right:
    st.subheader("🎵 ส่งคำขอเพลง")
    with st.form("song_request", clear_on_submit=True):
        u_name = st.text_input("👤 ชื่อของคุณ")
        u_song = st.text_input("🎶 ชื่อเพลง / ศิลปิน")
        submit = st.form_submit_button("ส่งคำขอเข้าสถานี 🚀")
        
        if submit:
            if u_name and u_song:
                # บันทึกข้อมูลลง Firebase
                db.collection('requests').add({
                    'name': u_name,
                    'song': u_song,
                    'time': datetime.datetime.now()
                })
                st.balloons()
                st.success("ส่งเรียบร้อย! ข้อมูลบันทึกลงฐานข้อมูลแล้ว")
            else:
                st.warning("กรุณากรอกข้อมูลให้ครบครับ")

# --- [ส่วนแสดงประวัติการขอเพลงจาก Firebase] ---
st.write("---")
st.subheader("📜 5 รายการขอเพลงล่าสุด (ดึงข้อมูลจริง)")

try:
    docs = db.collection('requests').order_by('time', direction=firestore.Query.DESCENDING).limit(5).get()
    for d in docs:
        data = d.to_dict()
        st.markdown(f"""
            <div class="song-card">
                <div class="user-name">👤 ผู้ขอ: {data['name']}</div>
                <div class="song-title">🎵 {data['song']}</div>
            </div>
        """, unsafe_allow_html=True)
except:
    st.write("ยังไม่มีข้อมูลคำขอเพลงในขณะนี้")
