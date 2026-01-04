import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="SYNAPSE: MASTER MIND", layout="wide", page_icon="🧠")

# ใส่ Key ของพี่ (อันเดียวกับที่เคยใช้)
# ถ้าไม่มี Key ให้ลบบรรทัด genai ออก แล้วใช้ระบบ Template แทนได้
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        has_ai = True
    else:
        has_ai = False
except:
    has_ai = False

# --- UI ---
st.title("🧠 SYNAPSE: Music Architect")
st.caption("ระบบออกแบบโครงสร้างเพลงอัจฉริยะ (ลิขสิทธิ์โดย S.S.W)")

# 1. Input ของพี่ (สั้นๆ ง่ายๆ)
col1, col2 = st.columns([1, 2])
with col1:
    mood = st.selectbox("อารมณ์เพลง", ["เศร้า/ดราม่า", "ให้กำลังใจ/พลัง", "รักโรแมนติก", "เดือด/ประชดชีวิต"])
    genre = st.selectbox("แนวเพลง", ["R&B Soul", "Modern Rock", "Thai Pop", "Dark Trap"])
with col2:
    concept = st.text_input("คอนเซปต์/ประโยคเด็ด", "อยู่นิ่งๆ ไม่เจ็บตัว")

# 2. THE BRAIN ENGINE (ถ้ามี AI ให้ AI คิด / ถ้าไม่มีใช้สูตรพี่)
if st.button("🚀 สั่งการระบบ (GENERATE BLUEPRINT)"):
    if has_ai:
        with st.status("🧠 SYNAPSE กำลังคำนวณโครงสร้างเพลง...", expanded=True):
            prompt = f"""
            Act as a professional Songwriter & Music Producer.
            Create a full song structure for:
            - Concept: "{concept}"
            - Mood: {mood}
            - Genre: {genre}
            
            Output Format (Strictly):
            1. [Song Title]: (Create a cool name)
            2. [Style Tags]: (For AI Generator e.g. Male vocals, slow tempo, 90bpm)
            3. [Lyrics]:
               - Verse 1: (Storytelling)
               - Pre-Chorus: (Build up)
               - Chorus: (Hook - impactful)
               - Verse 2: (Deepening)
               - Bridge: (Emotion peak)
               - Outro: (Fading thought)
            
            Make lyrics in THAI language. Deep, poetic, touching.
            """
            response = model.generate_content(prompt)
            st.success("✅ โครงสร้างเสร็จสมบูรณ์")
            st.markdown("---")
            st.markdown(response.text)
            
            # ปุ่ม Copy (จำลอง)
            st.info("💡 นำข้อมูลในช่อง [Style Tags] และ [Lyrics] ไปใส่ในเครื่องมือสร้างเสียงของคุณได้เลย")
            
    else:
        # กรณีไม่มี Key หรือ Key หมด (ใช้สูตร Template)
        st.warning("⚠️ ระบบ AI ออฟไลน์ -> ใช้โหมด Template มาตรฐาน")
        st.markdown(f"### 🎵 เพลง: {concept}")
        st.markdown(f"**Style:** {genre}, {mood}, Male Vocals, High Quality")
        st.markdown("---")
        st.text_area("Verse 1", "มองดูฟ้าที่กว้างใหญ่...\nใจดวงนี้มันล่องลอยไป...")
        st.text_area("Chorus", f"ก็แค่ {concept}...\nให้โลกมันหมุนไปตามกาลเวลา...")
        st.info("นี่คือโครงร่างพื้นฐาน พี่สามารถแก้เนื้อเพลงได้เลย")

st.markdown("---")
st.caption("System developed by S.S.W | Powered by Gemini API")
