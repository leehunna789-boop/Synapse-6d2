import streamlit as st
from pydub import AudioSegment
import io

# ตั้งชื่อหน้าเว็บ
st.set_page_config(page_title="Audio Mixer", page_icon="🎵")
st.header("เครื่องมือรวมเสียงร้อง + ดนตรี")

# ส่วนอัปโหลดไฟล์
vocal_file = st.file_uploader("1. อัปโหลดไฟล์เสียงร้อง (Vocal)", type=["wav", "mp3"])
instrument_file = st.file_uploader("2. อัปโหลดไฟล์ดนตรี (Instrument)", type=["wav", "mp3"])

if vocal_file and instrument_file:
    if st.button("เริ่มรวมเสียง"):
        with st.spinner("รอแป๊บนะ... กำลังผสมเสียงให้ครับ"):
            # โหลดไฟล์จากที่อัปโหลด
            vocal = AudioSegment.from_file(vocal_file)
            inst = AudioSegment.from_file(instrument_file)

            # รวมเสียงเข้าด้วยกัน
            combined = inst.overlay(vocal)

            # สร้างไฟล์สำหรับดาวน์โหลด
            out = io.BytesIO()
            combined.export(out, format="wav")
            
            st.success("รวมเสร็จแล้ว!")
            st.audio(out) # เปิดให้ฟังในเว็บได้เลย
            st.download_button("ดาวน์โหลดเพลงเต็ม", out.getvalue(), "final_song.wav")
