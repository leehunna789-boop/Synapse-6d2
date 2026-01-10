import streamlit as st
import google.generativeai as genai

# --- 1. ดึง API Key จากที่ซ่อน (Secrets) ---
try:
    # เรียกใช้ Key จากที่ซ่อน (GEMINI_API_KEY) เพื่อความปลอดภัย
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # แก้ Error 404: เปลี่ยนเป็นรุ่นปัจจุบันที่รองรับ
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("❌ ไม่พบ API Key ใน Secrets หรือตั้งชื่อไม่ตรง (ต้องใช้: GEMINI_API_KEY)")
    st.stop()

# --- 2. การตกแต่งหน้าตา (สีแดง น้ำเงิน เขียว ขาว นีออน) ---
st.markdown("""
    <style>
    .stApp { background-color: #000033; color: white; }
    .stButton>button { 
        background-color: #990000; color: white; border: 2px solid white; 
        font-weight: bold; border-radius: 12px; height: 3.5em; width: 100%;
        box-shadow: 0px 0px 10px #FF0000;
    }
    .stTextArea>div>div>textarea { 
        background-color: #001a00; color: white; border: 2px solid #00FF00; 
        border-radius: 10px; font-size: 1.1em;
    }
    .player-box { 
        background: linear-gradient(180deg, #000066 0%, #000033 100%);
        padding: 25px; border-radius: 20px; border: 3px solid #FF00FF; 
        margin-bottom: 30px; text-align: center;
    }
    h1 { text-shadow: 0 0 10px #FF0000, 0 0 20px #FF0000; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. เครื่องเล่นเพลงหน้ากลาง (เพลงของคุณเท่านั้น) ---
st.markdown('<div class="player-box">', unsafe_allow_html=True)
st.image("logo.jpg", width=250)
st.markdown("## 🎧 SYNAPSE PLAYER")
st.markdown("#### กำลังเล่น: เพลงพิเศษจากผู้สร้างแอป")
try:
    # เล่นเพลงของคุณที่คุณอัปโหลดไว้ในโฟลเดอร์แอป
    st.audio("music.mp3", loop=True)
    st.caption("🎶 เพลงนี้จะเล่นวนลูปไปทุกหน้าเพื่อให้คุณผ่อนคลาย")
except:
    st.warning("⚠️ อย่าลืมอัปโหลดไฟล์เพลงชื่อ music.mp3 เข้าไปในระบบด้วยนะครับ")
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. โครงสร้าง 4 หน้าหลัก (เน้นความแน่นและใช้งานง่าย) ---
tabs = st.tabs(["🔥 ระบายความในใจ", "🎸 เลือกแนวเพลง", "🎹 รับบทเพลงบำบัด", "🤝 คุยกับ AI"])

with tabs[0]:
    st.markdown("### กระดานระบายใจ")
    col_input, col_tool = st.columns([5, 1])
    with col_input:
        user_input = st.text_area("ปลดปล่อยความรู้สึกของคุณที่นี่...", height=350, placeholder="วันนี้คุณรู้สึกยังไงบ้าง?")
    with col_tool:
        st.write("เครื่องมือ")
        st.button("🧹 ล้าง")
        st.button("🔥 เผา")
        st.write(f"ตัวอักษร: {len(user_input)}")

with tabs[1]:
    st.markdown("### เลือกทำนองที่จะเยียวยาคุณ")
    genre = st.selectbox("สไตล์เพลง:", ["หมอลำ", "Pop", "Rock", "Rap", "เพื่อชีวิต", "ลูกทุ่ง", "R&B"])
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.button("🔈 ฟังตัวอย่าง")
    c2.button("🎲 สุ่มสไตล์")
    c3.button("🔥 ยอดนิยม")
    st.info("💡 เพลงที่คุณเลือกจะถูกใช้เป็นฐานในการแต่งเนื้อเพลงโดย AI")

with tabs[2]:
    st.markdown("### บทเพลงจาก 'อยู่นิ่งๆ ไม่เจ็บตัว'")
    if st.button("✨ เริ่มปรุงเพลงบำบัด (AI RUN)"):
        if user_input:
            with st.spinner("กำลังเปลี่ยนความทุกข์ของคุณให้เป็นตัวโน้ต..."):
                try:
                    prompt = f"คุณคือ อยู่นิ่งๆ ไม่เจ็บตัว แต่งเพลง {genre} จากข้อความ: {user_input} โดยใส่คอร์ดเพลงกำกับทุกประโยค"
                    response = model.generate_content(prompt)
                    st.code(response.text, language='text')
                    
                    st.divider()
                    st.write("🔓 ปลดล็อคปุ่มดาวน์โหลด:")
                    share1, share2 = st.columns(2)
                    share1.button("แชร์ลง Facebook")
                    share2.button("กดไลก์เพจ")
                except Exception as e:
                    st.error(f"AI มีปัญหาเล็กน้อย: {e}")
        else:
            st.error("กรุณาพิมพ์ความในใจที่หน้าแรกก่อนนะครับ")

with tabs[3]:
    st.markdown("### ปรึกษาปัญหากับ AI ส่วนตัว")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
        
    if chat_p := st.chat_input("คุยได้ทุกเรื่อง..."):
        st.session_state.messages.append({"role": "user", "content": chat_p})
        with st.chat_message("user"): st.write(chat_p)
        
        with st.spinner("อยู่นิ่งๆ กำลังพิมพ์..."):
            reply = model.generate_content(f"ตอบในฐานะเพื่อนบำบัด: {chat_p}").text
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"): st.write(reply)
