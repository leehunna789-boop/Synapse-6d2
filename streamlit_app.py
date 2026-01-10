import streamlit as st
import google.generativeai as genai
import os

# --- 1. ตั้งค่า API (ใช้รุ่นล่าสุด 1.5-flash) ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # เปลี่ยนจาก gemini-pro เป็นตัวนี้เพื่อให้หาย Error 404
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("กรุณาใส่ API Key ในหน้า Secrets ก่อน")
        st.stop()
except Exception as e:
    st.error(f"การเชื่อมต่อ AI ผิดพลาด: {e}")
    st.stop()

# --- 2. หน้าตาแอป ---
st.markdown("<style>.stApp { background-color: #000033; color: white; }</style>", unsafe_allow_html=True)

# --- 3. เครื่องเล่นเพลงหน้ากลาง ---
st.markdown("### 🎧 SYNAPSE PLAYER")
if os.path.exists("music.mp3"):
    # เช็กขนาดไฟล์เบื้องต้น
    if os.path.getsize("music.mp3") < 100:
        st.warning("⚠️ ไฟล์เพลง music.mp3 เสียหายหรือมีขนาดเล็กเกินไป (โปรดอัปโหลดใหม่ใน GitHub)")
    else:
        st.audio("music.mp3", loop=True)
        st.caption("🎶 เพลงกำลังเล่น... (ถ้าไม่ได้ยินให้กดปุ่ม Play)")
else:
    st.error("⚠️ ไม่พบไฟล์ music.mp3 ใน GitHub")

# --- 4. ส่วนเนื้อหา ---
tab1, tab2 = st.tabs(["📝 ระบายใจ/แต่งเพลง", "💬 คุยกับ AI"])

with tab1:
    msg = st.text_area("วันนี้เป็นยังไงบ้าง?", height=200)
    genre = st.selectbox("แนวเพลง", ["หมอลำ", "Pop", "Rock"])
    if st.button("✨ แต่งเพลงบำบัด"):
        if msg:
            with st.spinner("AI กำลังแต่งเพลง..."):
                res = model.generate_content(f"แต่งเพลงแนว {genre} จากเรื่อง: {msg}")
                st.code(res.text)
        else:
            st.warning("พิมพ์ข้อความก่อนครับ")

with tab2:
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.write(m["content"])
    if p := st.chat_input("คุยกับผม..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        # เรียก AI
        response = model.generate_content(p)
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"): st.write(response.text)
