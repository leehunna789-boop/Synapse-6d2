import streamlit as st
import numpy as np
import requests
import json

# --- 1. ตั้งค่าพื้นฐาน ---
st.set_page_config(page_title="Identity Sound Creator", page_icon="🎵")

# --- 2. ฟังก์ชันสร้างคลื่นเสียง (PCM 16-bit) ---
def generate_audio_signal(params):
    sample_rate = 44100
    duration = 2.5  # เล่นยาวขึ้นนิดนึงให้พอฟังทัน
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # ดึงค่าจาก AI (ถ้าไม่มีให้ใช้ค่าเริ่มต้น)
    freq = params.get('rbf1_freq', 440)
    gain = params.get('gain', 0.5)
    
    # สร้างเสียง (Sine wave พื้นฐาน)
    audio = gain * np.sin(2 * np.pi * freq * t)
    
    # ปรับระดับเสียงไม่ให้แตก
    audio_int16 = (audio * 32767).astype(np.int16)
    return audio_int16.tobytes()

# --- 3. หน้าตาแอป (UI) ---
st.title("🎵 Identity Sound Creator")
st.markdown("สโลแกน: **\"อยู่นิ่งๆ ไม่เจ็บตัว\"**")

api_key = st.text_input("ป้อน Gemini API Key ของคุณ:", type="password", help="รับคีย์ได้ที่ Google AI Studio")
user_input = st.text_area("อธิบายตัวตนของคุณ:", placeholder="เบื่อไม่เสร็จสักที...", height=100)

if st.button("สร้างเสียงตัวตน"):
    if not api_key or not user_input:
        st.warning("กรุณาใส่ข้อมูลให้ครบก่อนครับ")
    else:
        with st.spinner("AI กำลังวิเคราะห์... ใจเย็นๆ นะครับ"):
            try:
                # เชื่อมต่อ Gemini API
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                # โครงสร้างคำสั่ง (Prompt) ที่บังคับให้ AI ตอบเป็น JSON เท่านั้น
                prompt = (
                    f"วิเคราะห์ตัวตนนี้: '{user_input}' "
                    "แล้วตอบกลับเป็น JSON รูปแบบนี้เท่านั้น: "
                    "{'explanation': 'คำอธิบายสั้นๆ ภาษาไทย', 'rbf_parameters': {'gain': 0.5, 'rbf1_freq': 440}}"
                )
                
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"responseMimeType": "application/json"}
                }
                
                response = requests.post(api_url, json=payload)
                result = response.json()

                # ตรวจสอบว่ามีข้อมูลส่งกลับมาจริงไหม (ป้องกัน KeyError)
                if 'candidates' in result:
                    raw_text = result['candidates'][0]['content']['parts'][0]['text']
                    data = json.loads(raw_text)
                    
                    # แสดงผล
                    st.success("สำเร็จ!")
                    st.info(f"✨ {data.get('explanation', 'วิเคราะห์เสร็จสิ้น')}")
                    
                    # สร้างและเล่นเสียง
                    params = data.get('rbf_parameters', {})
                    audio_bytes = generate_audio_signal(params)
                    st.audio(audio_bytes, format="audio/wav", sample_rate=44100)
                    
                    # แสดงค่าที่ AI เจนออกมา (เผื่ออยากดู)
                    with st.expander("ดูค่าพารามิเตอร์"):
                        st.json(params)
                else:
                    # ถ้า AI ส่ง Error มา
                    error_msg = result.get('error', {}).get('message', 'ไม่ทราบสาเหตุ')
                    st.error(f"เกิดข้อผิดพลาดจาก AI: {error_msg}")
                    
            except Exception as e:
                st.error(f"ระบบขัดข้อง: {str(e)}")

st.divider()
st.caption("พัฒนาด้วย Streamlit & Gemini API | สโลแกนของคุณ: อยู่นิ่งๆ ไม่เจ็บตัว")
