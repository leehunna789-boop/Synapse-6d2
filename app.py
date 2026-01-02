import numpy as np
import streamlit as st
from scipy.io import wavfile
import google.generativeai as genai
import time

# --- การตั้งค่า AI (ใช้ Key อันเดียว) ---
# แนะนำให้ใส่ Key ใน Streamlit Secrets หรือช่อง Input ในแอป
def setup_ai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# -----------------------------------------------------------
# 1. INPUT MODULE (เชื่อมต่อกับ Gemini AI)
# -----------------------------------------------------------
class InputModule:
    ROOT_VOCAB = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11} 
    
    def ให้_AI_ช่วยแต่งเพลง(self, model, prompt):
        """ใช้ Gemini แปลงหัวข้อเป็น คอร์ด และ เนื้อเพลง"""
        full_prompt = f"""
        คุณคือนักแต่งเพลงมืออาชีพ ช่วยแต่งเพลงจากหัวข้อ: "{prompt}"
        ส่งคำตอบกลับมาเป็นรูปแบบ JSON เท่านั้นดังนี้:
        {{
            "lyrics": "เนื้อเพลงที่แต่ง",
            "chords": "C, G, Am, F",
            "valence": 0.8,
            "arousal": 0.7
        }}
        """
        response = model.generate_content(full_prompt)
        # หมายเหตุ: ในการใช้งานจริงควรมีตัว Parse JSON ที่ปลอดภัย
        return response.text

    def แปลง_คอร์ด_เป็น_ตัวเลข(self, chord_string):
        if not chord_string: return 0
        try:
            root = chord_string.strip().split()[0][:2].upper().replace('MAJ','').replace('MIN','')
            for k in self.ROOT_VOCAB:
                if root.startswith(k): return self.ROOT_VOCAB[k]
            return 0
        except: return 0

    def จัด_โครงสร้าง_คำสั่ง(self, chords_str, valence, arousal):
        chord_list = [c.strip() for c in chords_str.split(',')]
        total_length = len(chord_list) * 50
        symbolic_sequence = np.zeros((total_length, 3)) 
        for i, c in enumerate(chord_list):
            start, end = i * 50, (i + 1) * 50
            symbolic_sequence[start:end, 0] = self.แปลง_คอร์ด_เป็น_ตัวเลข(c)
        symbolic_sequence[:, 1] = valence
        symbolic_sequence[:, 2] = arousal
        return symbolic_sequence

# -----------------------------------------------------------
# 2. AI SYNTHESIS & 3. MASTERING (โครงเดิมที่คุณเขียนไว้)
# -----------------------------------------------------------
class AISynthesisEngine:
    def __init__(self, samplerate=44100):
        self.sampling_rate = samplerate

    def สังเคราะห์_ด้วย_รายละเอียด_RBF(self, symbolic_sequence):
        # จำลองการสร้าง MFCC Features
        return np.random.rand(symbolic_sequence.shape[0], 40) 

class MasteringModule:
    def ใช้_Limiter(self, audio, ceiling=0.99):
        return np.clip(audio, -ceiling, ceiling)

    def เขียน_ไฟล์เพลง_สุดท้าย(self, mfcc_features, samplerate=44100):
        # จำลองการแปลงเป็นเสียง Raw Audio
        audio_raw = np.random.uniform(-0.5, 0.5, int(samplerate * 5)) 
        audio_limited = self.ใช้_Limiter(audio_raw)
        final_audio = (audio_limited * 0.5 * 32767).astype(np.int16)
        return final_audio, samplerate

# -----------------------------------------------------------
# 4. MAIN APP LOGIC
# -----------------------------------------------------------
class RBAISystem:
    def __init__(self):
        self.input_module = InputModule()
        self.ai_engine = AISynthesisEngine()
        self.mastering_module = MasteringModule()

# -----------------------------------------------------------
# 5. STREAMLIT UI
# -----------------------------------------------------------
st.set_page_config(layout="wide", page_title="AI Music Composer")
st.title("🎵 แอปแต่งเพลงอัจฉริยะ (RBF AI + Gemini)")

# ช่องใส่ API Key
api_key = st.sidebar.text_input("ใส่ Gemini API Key เพื่อปลดล็อก", type="password")

if api_key:
    model = setup_ai(api_key)
    system = RBAISystem()

    st.header("1. บอกหัวข้อเพลงที่คุณอยากแต่ง")
    user_prompt = st.text_input("ตัวอย่าง: เพลงรักเศร้าๆ แนวฝนตก", "ความเหงาในเมืองใหญ่")

    if st.button("🚀 เริ่มแต่งเพลงและสังเคราะห์เสียง"):
        with st.spinner("AI กำลังแต่งเนื้อเพลงและคำนวณคอร์ด..."):
            # ขั้นตอน AI แต่งเนื้อหา
            raw_result = system.input_module.ให้_AI_ช่วยแต่งเพลง(model, user_prompt)
            st.info(f"AI Response: {raw_result}") # แสดงผลดิบเพื่อให้คุณเห็นการทำงาน
            
            # (ในตัวอย่างนี้ผมขอดึงค่า Default เพื่อให้รันต่อได้)
            chords = "C, G, Am, F" 
            
            # ขั้นตอนสังเคราะห์เสียง
            sym_seq = system.input_module.จัด_โครงสร้าง_คำสั่ง(chords, 0.5, 0.5)
            mfcc = system.ai_engine.สังเคราะห์_ด้วย_รายละเอียด_RBF(sym_seq)
            audio, sr = system.mastering_module.เขียน_ไฟล์เพลง_สุดท้าย(mfcc)
            
            st.success("แต่งเพลงเสร็จแล้ว!")
            st.audio(audio.astype(np.float32)/32767.0, format='audio/wav', sample_rate=sr)
else:
    st.warning("กรุณาใส่ API Key ใน Sidebar เพื่อเริ่มต้นใช้งาน")
    st.markdown("ถ้ายังไม่มี ไปเอาได้ที่ [Google AI Studio](https://aistudio.google.com/) ครับ")

