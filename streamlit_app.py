import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# --- [ส่วนเชื่อมต่อ Firebase] ---
if not firebase_admin._apps:
    try:
        # บรรทัดเหล่านี้ต้องย่อหน้าเข้ามา 1 ระดับ (4 spaces)
        key_dict = st.secrets["sooksun1"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred)
    except Exception as e:
        # คำว่า except ต้องอยู่ตรงแนวเดียวกับคำว่า try
        st.error(f"เชื่อมต่อฐานข้อมูลไม่ได้: {e}")

db = firestore.client()

# --- [ส่วนฟังก์ชันส่ง LINE Messaging API] ---
def send_push_notification(name, song):
    # 🚩 ใช้ค่าจาก Messaging API (Channel Access Token และ User ID)
    token = "4e96e8ceae54b81574dda897e7485faf"
    uid = "Ue7f8a054589e2d2996aae61dec7bf56c"
    
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    payload = {
        "to": uid,
        "messages": [{"type": "text", "text": f"📢 ขอเพลงใหม่!\n👤 จาก: {name}\n🎵 เพลง: {song}"}]
    }
    try:
        requests.post(url, headers=headers, json=payload)
    except:
        pass

# --- [ส่วนแสดงหน้าเว็บ Streamlit] ---
st.title("📻 สถานี 'อยู่นิ่งๆ ไม่เจ็บตัว'")
st.video("https://youtube.com/playlist?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO&si=LOTPiIS-KG5uLAwD") 

with st.form("song_request", clear_on_submit=True):
    u_name = st.text_input("ชื่อของคุณ")
    u_song = st.text_input("ชื่อเพลง")
    if st.form_submit_button("ส่งคำขอ"):
        if u_name and u_song:
            db.collection('requests').add({
                'name': u_name,
                'song': u_song,
                'time': datetime.datetime.now()
            })
            send_push_notification(u_name, u_song)
            st.success("ส่งเรียบร้อย!")

# แสดงประวัติการขอเพลง
docs = db.collection('requests').order_by('time', direction=firestore.Query.DESCENDING).limit(5).get()
for d in docs:
    data = d.to_dict()
    st.info(f"👤 {data['name']} - 🎵 {data['song']}")
