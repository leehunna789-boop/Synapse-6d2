import numpy as np
import streamlit as st
import google.generativeai as genai
import time

# --- ดีไซน์ม่วง-ดำ (SYNAPSE 6D) ---
st.set_page_config(page_title="SYNAPSE 6D Pro", layout="centered")
st.markdown("<style>.stApp { background-color: #0E1117; } h1, h2 { color: #B266FF !important; }</style>", unsafe_allow_html=True)

# --- ระบบ AI ---
genai.configure(api_key="AIzaSyBiKFHClySIV_UmeMznANnhyBoD78CYUrg")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- หน้าจอหลัก ---
st.title("💎 SYNAPSE : 6D ENERGY PRO")
st.write("สโลแกน: 'อยู่นิ่งๆ ไม่เจ็บตัว'")
mood = st.text_input("บอกความรู้สึกของคุณตอนนี้:")

if st.button("🚀 ACTIVATE ENERGY"):
    if mood:
        with st.spinner("กำลังจูนพลังงาน..."):
            response = model.generate_content(f"ให้คำแนะนำบวกๆ สำหรับคนที่รู้สึก: {mood}")
            st.success(response.text)
            st.audio(np.random.uniform(-1, 1, 44100*2), sample_rate=44100)
