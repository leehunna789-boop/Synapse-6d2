import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# --- [ส่วนที่ 1: ตั้งค่าหน้าตาแอป] ---
st.set_page_config(page_title="สถานีอยู่นิ่งๆ", page_icon="🎶")

# ตกแต่ง CSS ให้ดูแพง
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .song-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00ff00;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [ส่วนที่ 2: เชื่อมต่อ Firebase] ---
if not firebase_admin._apps:
    try:
        # ใช้ชื่อ 'sooksun1' ตามที่คุณตั้งใน Secrets
        key_dict = st.secrets["sooksun1"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"เชื่อมต่อฐานข้อมูลไม่ได้: {e}")

db = firestore.client()

# --- [ส่วนที่ 3: ฟังก์ชันส่งแจ้งเตือนแบบ Messaging API (ตัวใหม่)] ---
def send_push_notification(name, song):
    # 🚩 ต้องเอาค่า 2 อย่างนี้มาจาก LINE Developers Console
    channel_access_token = "ใส่_CHANNEL_ACCESS_TOKEN_ของคุณตรงนี้"
    user_id = "ใส่_USER_ID_ของคุณตรงนี้"
    
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}'
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": f"📢 คำขอเพลงใหม่!\n👤 จาก: {name}\n🎵 เพลง: {song}"
            }
        ]
    }
    try:
        requests.post(url, headers=headers, json=payload)
    except:
        pass

# --- [ส่วนที่ 4: หน้าเว็บหลัก] ---
st.title("📻 สถานี 'อยู่นิ่งๆ ไม่เจ็บตัว' (V.2)")
st.write("ยินดีต้อนรับสู่สถานีที่ฟังแล้วสบายใจที่สุด")

# เครื่องเล่นเพลง
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 

st.divider()

# ฟอร์มขอเพลง
st.subheader("🎵 อยากฟังเพลงอะไร ขอมาได้เลย")
with st.form("song_request", clear_on_submit=True):
    u_name = st.text_input("ชื่อของคุณ")
    u_song = st.text_input("ชื่อเพลงที่อยากฟัง")
    submit = st.form_submit_button("ส่งคำขอเพลง")

    if submit:
        if u_name and u_song:
            # 1. บันทึกลง Firebase
            db.collection('requests').add({
                'name': u_name,
                'song': u_song,
                'time': datetime.datetime.now()
            })
            # 2. ส่ง Push Message เข้า LINE (ระบบใหม่)
            send_push_notification(u_name, u_song)
            st.success("ส่งคำขอเรียบร้อยครับ!")
        else:
            st.warning("ใส่ข้อมูลให้ครบก่อนนะจ๊ะ")

# --- [ส่วนที่ 5: แสดงรายการล่าสุด] ---
st.divider()
st.subheader("📜 รายการขอเพลงล่าสุด")
try:
    docs = db.collection('requests').order_by('time', direction=firestore.Query.DESCENDING).limit(5).get()
    for d in docs:
        data = d.to_dict()
        st.markdown(f"""
        <div class="song-card">
            <b>{data['name']}</b> ขอเพลง <b>{data['song']}</b>
        </div>
        """, unsafe_allow_html=True)
except:
    st.write("ยังไม่มีข้อมูลในระบบ")
