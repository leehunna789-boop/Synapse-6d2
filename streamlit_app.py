import streamlit as st
import os
import random

# --- 1. ตั้งค่าพื้นฐาน ---
st.set_page_config(page_title="Synapse - อยู่นิ่งๆ ไม่เจ็บตัว", layout="wide")

# สร้างโฟลเดอร์เก็บเพลงถ้ายังไม่มี
MUSIC_FOLDER = "your_music.mp3"
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)

# --- 2. สไตล์สีเข้ม (ข้อ 7) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; border: 2px solid #FFFFFF; background-color: #1a1a1a; color: white; }
    h1, h2, h3, p { color: #FFFFFF !important; }
    /* ปรับแต่งช่อง Upload */
    .stFileUploader section { background-color: #111; border: 1px dashed #800080; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar และเครื่องเล่นเพลง ---
st.sidebar.title("📻 Synapse Player")
st.sidebar.image("logo.jpg")

# ดึงรายชื่อเพลง
def get_song_list():
    return [f for f in os.listdir(MUSIC_FOLDER) if f.lower().endswith(('.mp3', '.wav'))]

songs = get_song_list()
if songs:
    selected_song = st.sidebar.selectbox("เลือกเพลงบำบัด:", songs)
    with open(os.path.join(MUSIC_FOLDER, selected_song), 'rb') as f:
        st.sidebar.audio(f.read(), format='audio/mp3', loop=True)
st.sidebar.write("สโลแกน: **อยู่นิ่งๆ ไม่เจ็บตัว**")

# --- 4. เมนูหลัก 4 หน้า + หน้าจัดการเพลง ---
if 'page' not in st.session_state: st.session_state.page = "หน้า 1"

# เพิ่ม Tab "จัดการเพลง" เข้าไปเพื่อให้คุณอัปเดตเพลงได้หน้าแอปเลย
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 ระบายใจ", "🎸 เลือกแนว", "🎶 ผลงานเพลง", "💬 ปรับทุกข์", "📤 เพิ่มเพลง"])

# --- หน้า 5: เพิ่มเพลง (ระบบที่คุณต้องการ) ---
with tab5:
    st.header("📤 ระบบอัปเดตเพลง (สำหรับคุณเท่านั้น)")
    st.write("คุณสามารถอัปโหลดไฟล์ .mp3 เพิ่มเติมได้ที่นี่")
    uploaded_files = st.file_uploader("เลือกไฟล์เพลงจากมือถือของคุณ", type=['mp3', 'wav'], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(MUSIC_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success(f"อัปโหลดเพลงเรียบร้อยแล้ว {len(uploaded_files)} เพลง! (กรุณารีเฟรชหน้าเว็บ)")

# --- หน้า 1: ระบายความในใจ ---
with tab1:
    st.header("1. ระบายความในใจ")
    st.session_state.user_story = st.text_area("ปลดปล่อยความรู้สึกออกมา...", height=200)
    if st.button("พิมเสร็จแล้ว"):
        st.success("บันทึกแล้ว ไปเลือกแนวเพลงต่อเลย")

# --- หน้า 2: เลือกแนวเพลง ---
with tab2:
    st.header("2. เลือกแนวเพลง")
    genres = ["Pop", "Rock", "R&B", "Rap", "Hiphop", "ลูกทุ่ง", "เพื่อชีวิต", "หมอลำ"]
    cols = st.columns(2)
    for i, g in enumerate(genres):
        if cols[i%2].button(f"แนว {g}"):
            st.session_state.genre = g

# --- หน้า 3: รับเนื้อเพลง (ระบบบังคับแชร์) ---
with tab3:
    st.header("3. เนื้อเพลงจาก AI")
    if 'user_story' in st.session_state and 'genre' in st.session_state:
        # ระบบแต่งเพลงออฟไลน์
        chords = ["C", "G", "Am", "F"]
        lyrics = f"🎼 แนว: {st.session_state.genre}\n" + "-"*30 + "\n"
        for line in st.session_state.user_story.split('\n'):
            if line.strip():
                lyrics += f"({random.choice(chords)}) {line}\n"
        st.code(lyrics)
        
        st.write("📤 **แชร์ก่อนดาวน์โหลด**")
        if st.button("กดแชร์"):
            st.session_state.shared = True
        if st.session_state.get('shared'):
            st.download_button("💾 ดาวน์โหลดเพลง", lyrics, file_name="song.txt")
    else:
        st.write("กรุณากรอกข้อมูลหน้า 1 และ 2 ก่อน")

# --- หน้า 4: ปรับทุกข์ ---
with tab4:
    st.header("4. คุยกับ AI อยู่นิ่งๆ ไม่เจ็บตัว")
    chat = st.text_input("บอกความรู้สึกของคุณ...")
    if chat:
        st.write("🤖 AI: อยู่นิ่งๆ นะครับ ผมรับฟังคุณอยู่เสมอ...")
