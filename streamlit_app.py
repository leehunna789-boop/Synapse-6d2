import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
# ต้อง import library นี้เพิ่ม
from streamlit_player import st_player 

# --- [ตั้งค่าหน้าเว็บ] ---
st.set_page_config(page_title="สถานีอยู่นิ่งๆ ไม่เจ็บตัว", page_icon="📻", layout="wide")

# --- [ส่วน CSS ตกแต่ง] ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput>div>div>input { background-color: #262730; color: white; border-radius: 10px; }
    .stButton>button { 
        width: 100%; border-radius: 20px; background-color: #FF4B4B; color: white; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff3333; transform: scale(1.02); }
    .song-card {
        background-color: #1e2129; padding: 20px; border-radius: 15px; 
        margin-bottom: 15px; border-left: 6px solid #FF4B4B;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    .song-title { font-size: 1.2rem; font-weight: bold; color: #ffffff; }
    .user-name { color: #FF4B4B; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# --- [ส่วนเชื่อมต่อ Firebase] ---
if not firebase_admin._apps:
    try:
        key_dict = st.secrets["sooksun1"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"เชื่อมต่อฐานข้อมูลไม่ได้: {e}")

db = firestore.client()

# --- [ส่วนฟังก์ชันส่ง LINE] ---
def send_push_notification(name, song):
    # ตรวจสอบ URL ของ Line Messaging API ว่าต้องเป็น v2/bot/message/push
    token = "4e96e8ceae54b81574dda897e7485faf"
    uid = "Ue7f8a054589e2d2996aae61dec7bf56c"
    url = 'https://api.line.me'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
    payload = {
        "to": uid,
        "messages":[sooksun1]
    }
    try:
        requests.post(url, headers=headers, json=payload)
    except:
        pass

# --- [Layout หน้าเว็บ] ---
# ใช้ Sidebar เก็บรายละเอียดเล็กๆ
with st.sidebar:
    # แก้ URL รูปภาพโลโก้ให้ถูกต้อง
    st.image("https://cdn-icons-png.flaticon.com", width=100) 
    st.title("About Station")
    st.write("ยินดีต้อนรับสู่สถานีเพลงที่เงียบที่สุด (เพราะเราอยู่นิ่งๆ)")
    st.info("ส่งคำขอเพลงได้ตลอด 24 ชม.")

# แบ่งหน้าจอหลักเป็น 2 ฝั่ง
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.title("📻 สถานี 'อยู่นิ่งๆ ไม่เจ็บตัว📀'")
    
    # ใช้ st_player พร้อมลิงก์ Playlist ที่ถูกต้อง
    st_player("https://youtube.com") 

with col_right:
    st.subheader("🎵 ส่งคำขอเพลง")
    with st.form("song_request", clear_on_submit=True):
        u_name = st.text_input("👤 ชื่อของคุณ", placeholder="บอกชื่อหน่อยครับ...")
        u_song = st.text_input("🎶 ชื่อเพลง / ศิลปิน", placeholder="อยากฟังเพลงอะไรดี?")
        submit = st.form_submit_button("ส่งคำขอเข้าสถานี 🚀")
        
        if submit:
            if u_name and u_song:
                db.collection('requests').add({
                    'name': u_name,
                    'song': u_song,
                    'time': datetime.datetime.now()
                })
                send_push_notification(u_name, u_song)
                st.balloons() # เพิ่มเอฟเฟกต์ลูกโป่งตอนส่งสำเร็จ
                st.success("ส่งเรียบร้อย! ดีเจได้รับข้อมูลแล้ว")
            else:
                st.warning("กรุณากรอกข้อมูลให้ครบด้วยครับ")

# --- [ส่วนแสดงประวัติการขอเพลง] ---
st.write("---")
st.subheader("📜 5 รายการขอเพลงล่าสุด")

docs = db.collection('requests').order_by('time', direction=firestore.Query.DESCENDING).limit(5).get()

# แสดงผลแบบ Grid หรือ Card
for d in docs:
    data = d.to_dict()
    st.markdown(f"""
        <div class="song-card">
            <div class="user-name">👤 ผู้ขอ: {data['name']}</div>
            <div class="song-title">🎵 {data['song']}</div>
        </div>
    """, unsafe_allow_html=True)
