import streamlit as st

# --- หน้าตาเครื่องเล่นเพลงสไตล์ S.S.S 6D ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .neon-ring {
        width: 250px; height: 250px; margin: 0 auto;
        border: 5px solid #FF0000; border-radius: 50%;
        box-shadow: 0 0 20px #FF0000;
        display: flex; align-items: center; justify-content: center;
    }
    </style>
    <div class="neon-ring">
        <h1 style="color: white;">S.S.S</h1>
    </div>
""", unsafe_allow_html=True)

st.title("S.S.S Music 6D Player")

# --- ส่วนของเครื่องเล่นเพลง ---
# ลูกพี่เอาลิงก์ไฟล์เพลง (.mp3) มาใส่ตรงนี้ครับ
audio_file = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" 

st.write("🎵 กำลังรันระบบ: V1 Vocal / V2 6D Visual")
st.audio(audio_file, format='audio/mp3')

st.markdown("---")
st.write('"อยู่นิ่งๆ ไม่เจ็บตัว"')
