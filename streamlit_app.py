import streamlit as st
import google.generativeai as genai

# --- การดึง API Key จากที่ซ่อน (Secrets) ---
# เมื่อรันบน Streamlit Cloud ให้ตั้งชื่อใน Secrets ว่า GEMINI_API_KEY
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("⚠️ ไม่พบ API Key! กรุณาตั้งค่าใน Streamlit Secrets")

# ลิงก์ไฟล์ MP3 จาก GitHub (คุณสามารถเปลี่ยนเป็นลิงก์ของคุณได้เลย)
MUSIC_URL = "https://raw.githubusercontent.com/ชื่อUser/ชื่อProject/main/music.mp3"

# --- การตั้งค่าหน้าตาแอป ---
st.set_page_config(page_title="Synapse - อยู่นิ่งๆ ไม่เจ็บตัว", layout="centered")

# CSS ปรับแต่งสี (แดง น้ำเงิน เขียว ขาว)
st.markdown("""
    <style>
    .stApp { background-color: #0000FF; color: #FFFFFF; }
    h1, h2, h3 { color: #FFFFFF; text-shadow: 2px 2px #FF0000; }
    .stButton>button { 
        background-color: #FF0000; color: white; 
        border: 2px solid #FFFFFF; width: 100%; font-weight: bold; font-size: 20px;
    }
    div[data-testid="stTextArea"] textarea { background-color: #FFFFFF; color: #000; border: 5px solid #FF0000; font-size: 18px; }
    div[data-testid="stSelectbox"] div { background-color: #FFFFFF; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- โครงสร้างหน้าแอป (Tabs) ---
tab1, tab2, tab3 = st.tabs(["📝 1.ระบายความในใจ", "🎸 2.สร้างบทเพลง", "💬 3.คุยกับ AI"])

# หน้า 1: ระบายความในใจ
with tab1:
    st.title("SYNAPSE")
    st.subheader("อยู่นิ่งๆ ไม่เจ็บตัว")
    user_story = st.text_area("กระดานข้อความ: ละบายความในใจตามที่คุณต้องการ...", height=250)
    st.write("เมื่อระบายเสร็จแล้ว ให้กดไปที่เมนู 'สร้างบทเพลง' ด้านบน")

# หน้า 2 & 3: เลือกแนวเพลงและแสดงผลเนื้อเพลงพร้อมคอร์ด
with tab2:
    st.header("เลือกแนวเนื้อเพลง")
    genre = st.selectbox("แนวเพลงที่คุณชอบ:", 
                        ["Pop", "Rock", "R&B", "Rap", "Hip-hop", "ลูกทุ่ง", "เพื่อชีวิต", "หมอลำ"])
    
    if st.button("ขยายความให้เป็นบทเพลง"):
        if user_story:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"คุณคือ AI ชื่อ 'อยู่นิ่งๆไม่เจ็บตัว' จงนำข้อความนี้: '{user_story}' มาขยายความและแต่งเป็นเพลงแนว {genre} พร้อมระบุคอร์ดและคีย์เพลงในแต่ละประโยคให้ชัดเจน"
                
                with st.spinner('AI กำลังแต่งเพลง...'):
                    response = model.generate_content(prompt)
                    st.session_state.result = response.text
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณากลับไปพิมพ์ระบายที่หน้าแรกก่อนครับ")

    if 'result' in st.session_state:
        st.markdown("### 📄 เนื้อเพลงพร้อมคอร์ดจาก AI 'อยู่นิ่งๆ'")
        st.code(st.session_state.result, language="text")
        
        # ส่วนเสริมหน้า 4: ปุ่มแชร์และโหลด
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1: st.button("👍 กดไลค์")
        with col2: 
            if st.button("📢 กดแชร์เพื่อดาวน์โหลด"):
                st.session_state.shared = True
                st.success("ขอบคุณที่แชร์!")
        with col3:
            if st.session_state.get('shared', False):
                st.button("💾 ดาวน์โหลด")
            else:
                st.button("💾 ดาวน์โหลด (ต้องแชร์ก่อน)", disabled=True)

# หน้า 4 (เสริม): ปรับทุกข์กับ AI
with tab3:
    st.header("คุยกับ AI อยู่นิ่งๆ ไม่เจ็บตัว")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    if chat_input := st.chat_input("พูดคุยได้ทุกเรื่องแล้วแต่จะคุย..."):
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        with st.chat_message("user"): st.write(chat_input)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(chat_input)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"): st.write(response.text)

# --- หน้า 5: เครื่องเล่นเพลง (เล่นวนตลอดเวลา) ---
st.sidebar.markdown("### 🎵 Music Player")
st.sidebar.write("เล่นเพลงวนไปตลอดเวลาอัตโนมัติ")
st.sidebar.audio(MUSIC_URL, format="audio/mp3", loop=True)
