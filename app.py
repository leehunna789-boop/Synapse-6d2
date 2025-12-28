import numpy as np
import streamlit as st
import google.generativeai as genai
import json
import time

# --- 1. THE BRAIN: Gemini AI Emotional Decoder ---
# ตัวแปร v (Valence) และ a (Arousal) คือกุญแจสำคัญ
def decode_emotion(text):
    # จำลองการทำงานของ Gemini ที่แม่นยำที่สุด
    # v=0(เศร้า) -> 1(สุข), a=0(สงบ) -> 1(ตื่นเต้น)
    return {"v": 0.25, "a": 0.3, "weather": "Rainy"} 

# --- 2. THE ENGINE: Linear Interpolation (Lerp) ---
# นี่คือส่วนที่ทำให้มูลค่าสูงขึ้น เพราะมันทำให้การเปลี่ยนอารมณ์ "เนียน" เหมือนธรรมชาติ
def lerp(low, high, factor): return low + (high - low) * factor

# --- 3. THE TRANSFORMATION: Matrix Applied ---
def apply_synapse_matrix(data):
    v = data['v']
    
    # ดึงค่าจาก V1.0 (Vocal)
    f0 = lerp(0.3, 0.8, v)      # SAD -> JOY
    vib = lerp(0.2, 0.9, v)     # SAD -> JOY
    
    # ดึงค่าจาก V2.0 (Visual - 6 Parameters)
    sat = lerp(0.2, 0.9, v)
    light = lerp(0.3, 0.8, v)
    contrast = lerp(0.4, 0.8, v)
    dof = lerp(0.8, 0.3, v)     # ยิ่งเศร้า DOF ยิ่งสูง (หน้าชัดหลังเบลอเยอะ)
    texture = lerp(0.8, 0.7, v)
    focus = lerp(0.3, 0.9, v)
    
    return locals() # ส่งค่าทั้งหมดออกไปใช้งาน

# --- 4. THE UI: Immersive Interface ---
st.markdown("<h1 style='text-align: center; color: #ff0055;'>SYNAPSE: 100M Matrix Engine</h1>", unsafe_allow_html=True)

user_text = st.text_input("ระบุสภาวะของคุณเพื่อเริ่มการบำบัดด้วย Matrix...")

if st.button("🚀 EXECUTE MATRIX CONTROL"):
    with st.status("🔮 กำลังคำนวณ 3D Control Matrix...", expanded=True):
        raw_data = decode_emotion(user_text)
        matrix = apply_synapse_matrix(raw_data)
        time.sleep(1)
    
    # การแสดงผลแบบ Dashboard ห้องแล็บบำบัด
    st.write("### 🔊 Vocal Resonance (V1.0)")
    c1, c2 = st.columns(2)
    c1.metric("F0 Scalar", f"{matrix['f0']:.2f}")
    c2.metric("Vibrato Rate", f"{matrix['vib']:.2f}")
    
    st.write("### 🎨 Visual Environment (V2.0)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Saturation", f"{matrix['sat']:.2f}")
    col2.metric("Key Lighting", f"{matrix['light']:.2f}")
    col3.metric("Contrast", f"{matrix['contrast']:.2f}")
    
    col4, col5, col6 = st.columns(3)
    col4.metric("Depth of Field", f"{matrix['dof']:.2f}")
    col5.metric("Texture Detail", f"{matrix['texture']:.2f}")
    col6.metric("Composition Focus", f"{matrix['focus']:.2f}")
