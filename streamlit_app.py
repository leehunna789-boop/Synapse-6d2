import streamlit as st
import numpy as np
import requests
import json

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="Identity Sound Creator")

# 2. ฟังก์ชันสร้างเสียง (ห้ามลบย่อหน้าข้างหน้า)
def generate_audio(params):
    sr = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration), False)
    freq = params.get('rbf1_freq', 440)
    gain = params.get('gain', 0.5)
    
    # สร้างคลื่นเสียงพื้นฐาน
    audio = gain * np.sin(2 * np.pi * freq * t)
    return (audio * 32767).astype(np.int16).tobytes()

# 3. ส่วนแสดงผลบนหน้าเว็บ
st.title("🎵 Identity Sound Creator")
st.write("สโลแกน: **อยู่นิ่งๆ ไม่เจ็บตัว**")

api_key = st.text_input("ป้อน Gemini API Key:", type="password")
user_query = st.text_area("อธิบายตัวตนของคุณที่นี่:")

if st.button("เริ่มวิเคราะห์และสร้างเสียง"):
    if not api_key or not user_query:
        st.warning("กรุณากรอกข้อมูลให้ครบถ้วนก่อนครับ")
    else:
        with st.spinner("กำลังติดต่อ AI..."):
            try:
                # แก้ไขโครงสร้าง URL และ Payload ให้ถูกต้องตามมาตรฐาน Gemini
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + api_key
                
                # โครงสร้าง JSON ที่ถูกต้อง (ไม่มี "messages" แบบ OpenAI)
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": "Analyze identity: " + user_query + ". Output ONLY JSON: {'explanation': 'thai text', 'rbf_parameters': {'gain': 0.5, 'rbf1_freq': 440}}"
                        }]
                    }],
                    "generationConfig": {
                        "responseMimeType": "application/json"
                    }
                }

                response = requests.post(url, json=payload)
                result = response.json()

                # ดึงข้อมูลจาก JSON
                resp_text = result['candidates'][0]['content']['parts'][0]['text']
                data = json.loads(resp_text)

                st.success("วิเคราะห์เสร็จแล้ว!")
                st.write("---")
                st.info(data['explanation'])

                # เล่นเสียง
                audio_data = generate_audio(data['rbf_parameters'])
                st.audio(audio_data, format="audio/wav", sample_rate=44100)

            except Exception as e:
                st.error("เกิดข้อผิดพลาด: โปรดตรวจสอบ API Key หรือรูปแบบการเชื่อมต่อ")
                st.expander("ดูรายละเอียด Error").write(e)

st.divider()
st.caption("ระบบรันบน Streamlit - ปลอดภัย ไม่เจ็บตัว")
