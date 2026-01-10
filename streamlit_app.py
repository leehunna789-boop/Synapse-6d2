import streamlit as st
import google.generativeai as genai

# 1. เชื่อมต่อ AI (แก้เป็นรุ่น 1.5-flash เพื่อหายจาก Error 404)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("กรุณาเช็ก API Key ในหน้า Secrets")

# 2. ตั้งค่าหน้าตาแอป
st.set_page_config(page_title="SYNAPSE", layout="centered")
st.markdown("<style>.stApp { background-color: #000033; color: white; }</style>", unsafe_allow_html=True)

# 3. เครื่องเล่นเพลง (เพลงของคุณ) - วางไว้นอก Tab เพื่อให้ดังทุกหน้า
st.markdown("### 🎧 SYNAPSE PLAYER")
try:
    # เพิ่ม autoplay=True เพื่อให้เพลงพยายามเล่นเอง
    st.audio("music.mp3", loop=True, autoplay=True)
    st.caption("🎵 หากไม่ได้ยินเพลง ให้กดปุ่ม Play 1 ครั้งนะครับ")
except:
    st.warning("⚠️ ไม่พบไฟล์ music.mp3 ใน GitHub")

# 4. ส่วนเนื้อหาแอป
tabs = st.tabs(["🔥 ระบายใจ", "🎹 รับเพลง"])

with tabs[0]:
    user_text = st.text_area("วันนี้เป็นยังไงบ้าง?", height=300)

with tabs[1]:
    if st.button("✨ แต่งเพลงบำบัด"):
        if user_text:
            with st.spinner("กำลังแต่งเพลง..."):
                res = model.generate_content(f"แต่งเพลงจากเรื่องนี้: {user_text}")
                st.code(res.text)
        else:
            st.warning("พิมพ์ข้อความก่อนนะ")
