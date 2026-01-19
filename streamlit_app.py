import streamlit as st

st.title("⚙️ ตรวจเช็กเครื่องมือก่อนลงสนามจริง")

try:
    import pyworld as pw
    import librosa
    st.success("✅ ระบบพร้อม! pyworld และ librosa ติดตั้งเรียบร้อยแล้ว")
    st.info("ตอนนี้คุณสามารถรันโค้ด 'เนรมิตเสียง' ที่ผมให้ก่อนหน้านี้ได้ทันทีครับ")
except ImportError as e:
    st.error(f"❌ ระบบยังไม่พร้อม: {e}")
    st.warning("วิธีแก้: เพิ่มคำว่า pyworld และ librosa ลงในไฟล์ requirements.txt ใน GitHub ของคุณครับ")
