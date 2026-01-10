import streamlit as st
import google.generativeai as genai

# --- 1. ระบบดึง API Key จาก Secrets (ปลอดภัย ไม่ต้องวางรหัสในโค้ด) ---
try:
    # ดึงค่าจากหน้า Settings > Secrets ที่คุณตั้งชื่อว่า GEMINI_API_KEY
    key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=key)
    
    # แก้ Error 404: ใช้รุ่นล่าสุด gemini-1.5-flash
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("❌ ติดปัญหาเรื่อง API Key: กรุณาเช็กในหน้า Secrets")
    st.stop()

# --- 2. การตกแต่งหน้าตา (เข้มข้น: แดง น้ำเงิน เขียว ขาว) ---
st.set_page_config(page_title="SYNAPSE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000033; color: white; } /* พื้นหลังน้ำเงินเข้ม */
    .stButton>button { 
        background-color: #990000; color: white; border: 2px solid white; 
        font-weight: bold; border-radius: 12px; height: 3.5em; width: 100%;
    } /* ปุ่มแดง */
    .stTextArea>div>div>textarea { 
        background-color: #001a00; color: white; border: 2px solid #00FF00; 
    } /* ช่องกรอกเขียว */
    .player-box { 
        background: linear-gradient(180deg, #000066 0%, #000033 100%);
        padding: 20px; border-radius: 20px; border: 3px solid #FF00FF; 
        margin-bottom: 25px; text-align: center;
    } /* กรอบเครื่องเล่น */
    </style>
    """, unsafe_allow_html=True)

# --- 3. เครื่องเล่นเพลงหน้ากลาง (เพลงของคุณคนเดียว เพื่อนเปลี่ยนไม่ได้) ---
st.markdown('<div class="player-box">', unsafe_allow_html=True)
try:
    st.image("logo.jpg", width=200)
    st.markdown("### 🎧 SYNAPSE PLAYER")
    st.audio("music.mp3", loop=True) # เล่นเพลงที่คุณอัปโหลดไว้คนเดียว
    st.caption("🎶 เพลงพิเศษที่คุณเลือกให้เพื่อนๆ ฟัง (ดังต่อเนื่องทุกหน้า)")
except:
    st.warning("⚠️ อย่าลืมอัปโหลดไฟล์ music.mp3 และ logo.jpg เข้าไปในระบบ")
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. ส่วนเนื้อหา 4 หน้าหลัก ---
tabs = st.tabs(["🔥 ระบายใจ", "🎷 เลือกแนวเพลง", "🎹 รับบทเพลง", "🤝 คุยกับ AI"])

with tabs[0]:
    st.header("พื้นที่ปลดปล่อยความอัดอั้น")
    user_input = st.text_area("วันนี้เป็นยังไงบ้าง? ระบายออกมาให้หมด...", height=300)
    st.button("🧹 ล้างข้อความ")

with tabs[1]:
    st.header("เลือกท่วงทำนองบำบัด")
    genre = st.selectbox("สไตล์ดนตรีที่ต้องการ:", ["หมอลำ", "Pop", "Rock", "Rap", "ลูกทุ่ง", "เพื่อชีวิต"])
    st.info("💡 เมื่อเลือกแล้ว AI จะแต่งเนื้อเพลงตามแนวนี้ให้คุณ")

with tabs[2]:
    st.header("บทเพลงบำบัดจาก AI")
    if st.button("✨ สั่งให้ 'อยู่นิ่งๆ ไม่เจ็บตัว' แต่งเพลง"):
        if user_input:
            with st.spinner("กำลังเปลี่ยนความทุกข์เป็นเสียงเพลง..."):
                prompt = f"คุณคือ อยู่นิ่งๆ ไม่เจ็บตัว แต่งเพลง {genre} จากเนื้อหา: {user_input} พร้อมใส่คอร์ดเพลงกำกับ"
                response = model.generate_content(prompt)
                st.code(response.text, language='text')
                st.divider()
                st.button("🔗 แชร์ลง Facebook เพื่อปลดล็อคดาวน์โหลด")
        else:
            st.error("กรุณากลับไปพิมพ์ระบายใจในหน้าแรกก่อน")

with tabs[3]:
    st.header("ปรึกษาส่วนตัวกับ AI")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
        
    if chat_p := st.chat_input("คุยกับผมได้ทุกเรื่อง..."):
        st.session_state.messages.append({"role": "user", "content": chat_p})
        with st.chat_message("user"): st.write(chat_p)
        
        reply = model.generate_content(f"ตอบกลับแบบเพื่อนที่เข้าใจที่สุด: {chat_p}").text
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"): st.write(reply)
