import streamlit as st
import google.generativeai as genai

# --- 1. ดึงกุญแจที่ซ่อนไว้ (Secrets) ---
try:
    # ชื่อใน [] ต้องตรงกับที่ลูกพี่พิมพ์ในหน้า Secrets ของ Streamlit นะครับ
    API_KEY = st.secrets["GEMINI_KEY"] 
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("หา 'กุญแจ' ที่ซ่อนไว้ไม่เจอครับลูกพี่ อย่าลืมไปใส่ในเมนู Secrets นะ!")

# --- 2. แต่งหน้าตาให้เท่ (UI) ---
st.set_page_config(page_title="SYNAPSE 6D Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { 
        background-color: #FF0000; color: white; border-radius: 10px; 
        height: 60px; font-weight: bold; border: 2px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("S.S.S Music 6D")
st.write('สโลแกน: "อยู่นิ่งๆ ไม่เจ็บตัว"')

# --- 3. ส่วนรับใจความ ---
user_note = st.text_input("ใส่ความรู้สึกที่นี่...", placeholder="อารมณ์เฉยๆเพราะโดนหลอกมาเยอะ")

# --- 4. ปุ่มขยี้ (Logic) ---
if st.button("ขยี้ใจความ (GENERATE)", type="primary"):
    if user_note:
        with st.spinner("6D Matrix กำลังทำงาน..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"ขยี้ใจความว่า '{user_note}' ให้เป็นเนื้อเพลง 1 ท่อนที่คมๆ สไตล์คนผ่านโลกมาเยอะ และปิดท้ายด้วย 'อยู่นิ่งๆ ไม่เจ็บตัว'"
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("🎵 ผลลัพธ์จากการขยี้")
                st.success(response.text)
                st.info("📊 สถานะ: ดึงกุญแจสำเร็จ | ประมวลผล Matrix V1-V2 ครบถ้วน")
            except Exception as e:
                st.error(f"ระบบมีปัญหา: {e}")
    else:
        st.warning("ใส่ข้อความก่อนครับลูกพี่!")
