import streamlit as st
import google.generativeai as genai
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import matplotlib

# --- [ส่วนที่ 1: ตั้งค่าระบบ] ---
matplotlib.use('Agg')
st.set_page_config(page_title="SYNAPSE", page_icon="🌐")

# วางโลโก้
try:
    st.image("logo.jpg", width=200)
except:
    pass # ถ้าไม่มีโลโก้ก็ข้ามไป ไม่ต้องแจ้งเตือน

# ตั้งค่า API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- [ส่วนที่ 2: ตั้งค่าโมเดล Gemini] ---
instruction = (
    "คุณคือนักแต่งเพลง แนว Industrial/Dark Minimalist "
    "สโลแกน: 'อยู่นิ่งๆ ไม่เจ็บตัว' "
    "กฎ: แต่งเนื้อเพลงสั้นๆ 4 บรรทัด พร้อมคอร์ด และข้อความฮีลใจตอนท้าย"
)
model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=instruction)

# --- [ส่วนที่ 3: Engine เสียงใหม่ (ใช้ Numpy ล้วน ไม่ต้องใช้ pyworld)] ---
def synapse_lite_engine(duration, fs, mood_valence):
    t = np.linspace(0, duration, int(fs * duration))
    
    # 1. เทคนิค Solfeggio Frequencies (คลื่นเสียงบำบัดโบราณ)
    # 174Hz = ลดความเจ็บปวด / 396Hz = ขจัดความกลัว
    base_freq = 174 if mood_valence < 0.5 else 396
    
    # 2. Additive Synthesis: สร้างเสียงให้หนาขึ้น ไม่แบนแต๊ดแต๋
    # สร้าง 3 ชั้นเสียง: เบสต่ำ (Low), เสียงหลัก (Mid), เสียงแหลม (High)
    layer_low  = 0.6 * np.sin(2 * np.pi * (base_freq * 0.5) * t) # เสียงเบสลึกๆ
    layer_mid  = 0.4 * np.sin(2 * np.pi * base_freq * t)        # เสียงหลัก
    layer_high = 0.1 * np.sin(2 * np.pi * (base_freq * 2.0) * t) # เสียงกังวาน
    
    # รวมชั้นเสียง
    composite_wave = layer_low + layer_mid + layer_high

    # 3. LFO Breathing (เทคนิคทำให้เสียง "หายใจ" ได้)
    # ทำให้เสียงค่อยๆ ดัง-เบา ช้าๆ เหมือนชีพจร (จังหวะ 0.2 Hz)
    breathing = 0.8 + 0.2 * np.sin(2 * np.pi * 0.2 * t)
    composite_wave = composite_wave * breathing

    # 4. Binaural Detuning (แยกประสาทหูซ้าย-ขวา)
    # หูซ้าย: เสียงปกติ
    left_channel = composite_wave
    
    # หูขวา: บิดคลื่นนิดหน่อยให้สมองงงและสร้างคลื่น Alpha/Theta เอง (ผ่อนคลาย)
    beat_freq = 6 # Hz (Theta Wave)
    # สร้างคลื่นหูขวาโดยขยับความถี่นิดเดียว
    right_channel = (0.6 * np.sin(2 * np.pi * ((base_freq * 0.5) + beat_freq) * t)) + \
                    (0.4 * np.sin(2 * np.pi * (base_freq + beat_freq) * t))
    right_channel = right_channel * breathing

    # 5. ใส่ "Noise" (เสียงซ่าๆ) เล็กน้อย ให้ดูเป็นแนว Industrial/Lo-fi
    noise = np.random.normal(0, 0.01, len(t))
    
    # รวมร่าง
    audio_stereo = np.vstack((left_channel + noise, right_channel + noise)).T
    
    # ข้อมูลสำหรับกราฟ (Visual)
    f0_mock = base_freq + (breathing * 20) # กราฟเส้นจะขยับตามการหายใจ
    sp_mock = np.abs(np.fft.rfft(left_channel[:2048])) 

    return audio_stereo, f0_mock, sp_mock
# --- [ส่วนที่ 4: UI] ---
st.title("🌐 SYNAPSE: Lite Core")
st.caption("Mode: Frequency Therapy (No Vocoder)")

user_note = st.text_input("ระบุสิ่งที่กวนใจคุณ...", placeholder="EXECUTE YOUR PAIN HERE...")

if st.button("EXECUTE & HEAL"):
    if user_note:
        with st.spinner('Accessing Neural Network...'):
            # 1. Gemini แต่งเพลง
            try:
                response = model.generate_content(user_note)
                st.subheader("🎵 Text Output")
                st.write(response.text)
            except:
                st.error("API Key มีปัญหา หรือเน็ตหลุด")

            # 2. สร้างเสียงบำบัด
            fs = 44100
            duration = 10 # วินาที
            mood = 0.3 if "เจ็บ" in user_note or "เศร้า" in user_note else 0.8
            
            y, f0, sp = synapse_lite_engine(duration, fs, mood)
            
            # 3. บันทึกและเล่น
            output_path = "synapse_signal.wav"
            sf.write(output_path, y, fs)
            
            # 4. แสดงผล
            st.audio(output_path)
            
            # กราฟ
            fig, ax = plt.subplots(2, 1, figsize=(10, 6), facecolor='#0e1117')
            
            # กราฟบน (Pitch)
            ax[0].plot(f0[:1000], color='#00ff00', linewidth=1) # สีเขียว Terminal
            ax[0].set_facecolor('#0e1117')
            ax[0].set_title("Frequency Stability", color='white')
            ax[0].tick_params(colors='white')
            
            # กราฟล่าง (Spectrum)
            ax[1].plot(sp, color='#ff00ff', linewidth=1) # สีม่วง Neon
            ax[1].set_facecolor('#0e1117')
            ax[1].set_title("Energy Spectrum", color='white')
            ax[1].tick_params(colors='white')
            
            st.pyplot(fig)
            st.success("Process Complete. Stay Still.")
            
    else:
        st.warning("Input required.")
