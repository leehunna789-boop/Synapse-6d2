import streamlit as st
import google.generativeai as genai
import os

# --- 1. แก้ไขจุดที่ Error 404 (เปลี่ยนเป็นรุ่นล่าสุดให้แล้วครับ) ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # ผมแก้จาก gemini-pro เป็น gemini-1.5-flash ให้แล้วครับ
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("❌ หา API Key ไม่เจอในหน้า Secrets")
        st.stop()
except Exception as e:
    st.error(f"❌ ระบบเชื่อมต่อ AI ไม่ได้: {e}")
    st.stop()

# --- 2. ตั้งค่าหน้าตาแอป ---
st.set_page_config(page_title="SYNAPSE", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000033; color: white; }
    .stButton>button { background-color: #990000; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. เครื่องเล่นเพลงหน้ากลาง (จะติดถ้าอัปโหลดไฟล์เพลงสำเร็จ) ---
st.markdown("### 🎧 SYNAPSE PLAYER")
if os.path.exists("music.mp3"):
    # เช็กว่าไฟล์ไม่ใช่ 1 Byte (ถ้าไฟล์จริงต้องใหญ่กว่านี้)
    if os.path.getsize("music.mp3") > 100:
        st.audio("music.mp3", loop=True)
        st.caption("🎵 เพลงกำลังเล่น... (ถ้าไม่ได้ยินให้กดปุ่ม Play)")
    else:
        st.warning("⚠️ ไฟล์เพลงใน GitHub มีขนาด 1 Byte (อัปโหลดไม่สำเร็จ) โปรดลบแล้วอัปโหลดใหม่ครับ")
else:
    st.error("⚠️ ไม่พบไฟล์ชื่อ music.mp3 ใน GitHub")

# --- 4. ส่วนการใช้งาน ---
tab1, tab2 = st.tabs(["📝 ระบายใจ & แต่งเพลง", "💬 คุยกับ AI"])

with tab1:
    user_thought = st.text_area("วันนี้เป็นยังไงบ้าง? ระบายมาเลย...", height=200)
    genre = st.selectbox("เลือกแนวเพลง:", ["หมอลำ", "Pop", "Rock", "Rap"])
    if st.button("✨ ให้ AI แต่งเพลงให้ฉัน"):
        if user_thought:
            with st.spinner("กำลังแต่งเพลง..."):
                # เรียกใช้รุ่นใหม่ที่แก้ให้แล้ว
                response = model.generate_content(f"แต่งเพลงแนว {genre} จากเรื่อง: {user_thought} พร้อมใส่คอร์ด")
                st.code(response.text)
        else:
            st.warning("กรุณาพิมพ์ข้อความก่อนครับ")

with tab2:
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    if p := st.chat_input("คุยกับผมได้ทุกเรื่อง..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        # AI ตอบโต้ (ใช้รุ่นใหม่ล่าสุด)
        ai_resp = model.generate_content(p)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_resp.text})
        with st.chat_message("assistant"): st.write(ai_resp.text)
