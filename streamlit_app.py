import streamlit as st
import google.generativeai as genai
import os

# 1. ตั้งค่า API (ใช้รุ่นล่าสุด 1.5-flash เท่านั้น)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # ตัวนี้คือรุ่นใหม่ล่าสุดที่ Google ให้ใช้ฟรีและเสถียรครับ
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("กรุณาใส่ API Key ในหน้า Secrets ก่อน")
        st.stop()
except Exception as e:
    st.error(f"การเชื่อมต่อ AI ผิดพลาด: {e}")
    st.stop()

# 2. ปรับหน้าตาแอป (สีน้ำเงินเข้มตามสไตล์คุณ)
st.markdown("<style>.stApp { background-color: #000033; color: white; }</style>", unsafe_allow_html=True)

# 3. เครื่องเล่นเพลง (เพลงของคุณคนเดียว)
st.markdown("### 🎧 SYNAPSE PLAYER")
if os.path.exists("music.mp3"):
    if os.path.getsize("music.mp3") < 1000: # เช็กถ้าไฟล์เล็กผิดปกติ
        st.warning("⚠️ ไฟล์เพลงใน GitHub เสียหาย (ขนาดเล็กเกินไป) โปรดลบแล้วอัปโหลดใหม่")
    else:
        st.audio("music.mp3", loop=True)
        st.caption("🎵 เพลงจากผู้สร้าง (หากไม่ได้ยินให้กดปุ่ม Play)")
else:
    st.error("⚠️ ไม่พบไฟล์ music.mp3 ใน GitHub ของคุณ")

# 4. หน้าใช้งาน (จัดใหม่ให้แน่น ไม่โหลงเหลง)
tab1, tab2 = st.tabs(["📝 ระบายใจ & แต่งเพลง", "💬 คุยกับ AI"])

with tab1:
    msg = st.text_area("วันนี้เป็นยังไงบ้าง? ระบายมาเลย...", height=200)
    genre = st.selectbox("เลือกแนวเพลง:", ["หมอลำ", "Pop", "Rock", "Rap"])
    if st.button("✨ แต่งเพลงบำบัด"):
        if msg:
            with st.spinner("AI กำลังแต่งเพลงให้คุณ..."):
                response = model.generate_content(f"แต่งเพลงแนว {genre} จากเรื่อง: {msg} พร้อมใส่คอร์ด")
                st.code(response.text)
        else:
            st.warning("กรุณาพิมพ์ข้อความก่อนกดปุ่มครับ")

with tab2:
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    if p := st.chat_input("ระบายทุกข์กับ AI..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        
        # เรียก AI มาตอบ
        ai_resp = model.generate_content(p)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_resp.text})
        with st.chat_message("assistant"): st.write(ai_resp.text)
