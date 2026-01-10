import streamlit as st
import google.generativeai as genai

# --- การตั้งค่าเบื้องต้น ---
st.set_page_config(page_title="Synapse - อยู่นิ่งๆ ไม่เจ็บตัว", layout="wide")

# ดึง API Key จาก Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("ไม่พบ API Key ในระบบ หรือ Key ไม่ถูกต้อง")

# --- ข้อ 7: ตกแต่งโทนสีเข้มจัด ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; font-size: 18px; border: 2px solid #FFFFFF; }
    /* สีพื้นหลังปุ่มตามโจทย์ */
    div.stButton > button:first-child { background-color: #FF0000; color: white; } /* แดง */
    h1, h2, h3, p { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ข้อ 5: เครื่องเล่น MP3 เล่นวนตลอดเวลา ---
st.sidebar.image("logo.jpg")
st.sidebar.title("Synapse Player")
st.sidebar.write("🎵 กำลังเล่นเพลงบำบัดอัตโนมัติ")
try:
    audio_file = open('your_music.mp3', 'rb') # เปลี่ยนชื่อไฟล์ให้ตรงกับที่คุณมี
    audio_bytes = audio_file.read()
    st.sidebar.audio(audio_bytes, format='audio/mp3', start_time=0, loop=True)
except FileNotFoundError:
    st.sidebar.warning("ไม่พบไฟล์ your_music.mp3 กรุณาตรวจสอบชื่อไฟล์")

# --- ข้อ 6: ระบบจัดการหน้าจอ (4 หน้า) ---
if 'page' not in st.session_state:
    st.session_state.page = "หน้า 1"

tab1, tab2, tab3, tab4 = st.tabs(["📝 ระบายใจ", "🎸 เลือกแนว", "🎶 รับบทเพลง", "💬 คุยกับ AI"])

# --- หน้า 1: ระบายความในใจ ---
with tab1:
    st.header("1. กระดานระบายความในใจ")
    user_story = st.text_area("ปลดปล่อยความรู้สึกออกมาให้เต็มที่...", height=250, key="story_input")
    if st.button("พิมเสร็จแล้ว"):
        st.session_state.user_story = user_story
        st.success("บันทึกเรื่องราวแล้ว! กรุณากดไปที่หน้า 'เลือกแนว' ต่อไป")

# --- หน้า 2: เลือกแนวเพลง ---
with tab2:
    st.header("2. เลือกแนวเพลงที่คุณชอบ")
    genres = ["Pop", "Rock", "R&B", "Rap", "HipHop", "ลูกทุ่ง", "เพื่อชีวิต", "หมอลำ"]
    cols = st.columns(4)
    for i, genre in enumerate(genres):
        if cols[i % 4].button(genre):
            st.session_state.selected_genre = genre
            st.balloons()
            st.info(f"คุณเลือกแนว: {genre} เรียบร้อยแล้ว!")

# --- หน้า 3: แสดงผลลัพธ์ (AI อยู่นิ่งๆ ไม่เจ็บตัว) ---
with tab3:
    st.header("3. บทเพลงจาก 'อยู่นิ่งๆ ไม่เจ็บตัว'")
    if 'user_story' in st.session_state and 'selected_genre' in st.session_state:
        if st.button("เริ่มแต่งเพลงบำบัด"):
            with st.spinner("AI กำลังเรียบเรียงทำนองชีวิต..."):
                prompt = f"""จงแปลงความในใจนี้: '{st.session_state.user_story}' 
                ให้กลายเป็นบทเพลงแนว {st.session_state.selected_genre} 
                โดยมีโครงสร้าง เนื้อเพลง พร้อมใส่คอร์ดกีตาร์และคีย์เพลงกำกับในทุกประโยค
                ใช้สไตล์การเขียนแบบบำบัดจิตใจ ภายใต้คอนเซปต์ 'อยู่นิ่งๆ ไม่เจ็บตัว'"""
                
                response = model.generate_content(prompt)
                st.session_state.generated_lyrics = response.text
                
        if 'generated_lyrics' in st.session_state:
            st.text_area("เนื้อเพลงของคุณ:", value=st.session_state.generated_lyrics, height=400)
            
            # ข้อ 4: ระบบบังคับแชร์
            st.warning("🔒 คุณต้องกดแชร์ก่อนจึงจะดาวน์โหลดได้")
            col_like, col_share = st.columns(2)
            col_like.button("👍 ถูกใจ / ติดตาม")
            if col_share.button("📤 กดเพื่อแชร์"):
                st.session_state.is_shared = True
                st.success("ขอบคุณที่แชร์! ปลดล็อกปุ่มดาวน์โหลดแล้ว")
            
            if st.session_state.get('is_shared', False):
                st.download_button("💾 ดาวน์โหลดข้อมูลเพลง", st.session_state.generated_lyrics, "my_song.txt")
    else:
        st.write("กรุณาเขียนความในใจและเลือกแนวเพลงก่อนครับ")

# --- หน้า 4: หน้าเสริม ปรับทุกข์กับ AI ---
with tab4:
    st.header("4. ปรึกษา AI อยู่นิ่งๆ ไม่เจ็บตัว")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt_chat := st.chat_input("คุยได้ทุกเรื่อง..."):
        st.session_state.messages.append({"role": "user", "content": prompt_chat})
        with st.chat_message("user"):
            st.markdown(prompt_chat)

        with st.chat_message("assistant"):
            full_prompt = f"คุณคือ AI ชื่อ 'อยู่นิ่งๆ ไม่เจ็บตัว' ทำหน้าที่รับฟังและปลอบโยนคนเศร้า ตอบกลับคำถามนี้: {prompt_chat}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
