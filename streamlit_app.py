import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# --- [ส่วนที่ 1: ตั้งค่าหน้าตาเว็บ] ---
st.set_page_config(page_title="สถานีอยู่นิ่งๆ", page_icon="🎶", layout="centered")

# ตกแต่ง CSS ให้ดูดีขึ้น
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; border: none; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .song-box { padding: 20px; border-radius: 15px; background-color: #ffffff; border-left: 5px solid #ff4b4b; margin-bottom: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- [ส่วนที่ 2: เชื่อมต่อ Firebase] ---
# ดึงค่าจาก st.secrets["sooksun1"] ที่คุณแปะไว้ในหน้าเว็บ Streamlit
if not firebase_admin._apps:
    try:
        key_dict = st.secrets["sooksun1"]
        cred = credentials.Certificate(dict(key_dict))
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"❌ ระบบเชื่อมต่อฐานข้อมูลขัดข้อง: {e}")

db = firestore.client()

# --- [ส่วนที่ 3: ฟังก์ชันส่ง LINE Notify] ---
def send_line(message):
    # 🚩 เอา LINE Token ที่ขอมาวางตรงนี้ครับ 🚩
    line_token = "ใส่_LINE_TOKEN_ของคุณตรงนี้" 
    
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_token}'}
    try:
        requests.post(url, headers=headers, data={'message': message})
    except:
        pass

# --- [ส่วนที่ 4: หน้าตาแอปและเครื่องเล่นเพลง] ---
st.title("🎶 สถานี 'อยู่นิ่งๆ ไม่เจ็บตัว'")
st.write("สถานีวิทยุออนไลน์ของช่างใหญ่ เปิดเพลงตามใจคนฟัง")

# วิดีโอเพลง (เปลี่ยน URL เป็นเพลงที่อยากให้เปิดค้างไว้ได้เลย)
st.subheader("📻 กำลังรับฟัง")
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 

st.markdown("---")

# --- [ส่วนที่ 5: ระบบขอเพลง] ---
st.subheader("📝 ส่งคำขอเพลงถึงช่างใหญ่")
with st.form("request_form", clear_on_submit=True):
    u_name = st.text_input("ชื่อเล่นของคุณ (หรือนามแฝง)")
    u_song = st.text_input("ชื่อเพลง / ศิลปิน / หรือลิงก์เพลง")
    submit = st.form_submit_button("ส่งคำขอเพลงให้ช่างใหญ่ 🚀")

    if submit:
        if u_name and u_song:
            # 1. บันทึกลง Firebase
            doc_data = {
                'name': u_name,
                'song': u_song,
                'time': datetime.datetime.now()
            }
            db.collection('requests').add(doc_data)
            
            # 2. ส่งแจ้งเตือนเข้า LINE
            line_msg = f"\n📢 มีคนขอเพลงใหม่!\n👤 จาก: {u_name}\n🎵 เพลง: {u_song}"
            send_line(line_msg)
            
            st.success(f"ส่งคำขอเรียบร้อย! รอฟังได้เลยครับคุณ {u_name}")
        else:
            st.warning("⚠️ กรุณากรอกชื่อและชื่อเพลงก่อนส่งนะครับ")

# --- [ส่วนที่ 6: แสดงรายการที่ขอมาล่าสุด] ---
st.markdown("---")
st.subheader("📜 5 รายการล่าสุดที่ขอมา")

try:
    # ดึงข้อมูลจาก Firebase มาโชว์
    docs = db.collection('requests').order_by('time', direction=firestore.Query.DESCENDING).limit(5).get()
    
    if len(docs) > 0:
        for d in docs:
            item = d.to_dict()
            st.markdown(f"""
            <div class="song-box">
                <b>👤 {item.get('name')}</b> ขอมาเมื่อ {item.get('time').strftime('%H:%M น.')}<br>
                🎵 เพลง: {item.get('song')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("ยังไม่มีใครขอเพลงเลย ช่างใหญ่เหงามาก!")
except Exception as e:
    st.write("กำลังโหลดข้อมูลคำขอเพลง...")
