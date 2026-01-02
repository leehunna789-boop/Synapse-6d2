import streamlit as st
import numpy as np
import io
from scipy.io.wavfile import write
import random

# ---------------------------------------------------------
# 1. UI CONFIGURATION (DARK & RAW MODE)
# ---------------------------------------------------------
st.set_page_config(page_title="SYS_AUDIO_CORE", page_icon="◾", layout="wide")

st.markdown("""
<style>
    /* นำเข้าฟอนต์สไตล์ Coding */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&display=swap');

    .stApp { 
        background-color: #000000; 
        color: #B0B0B0; 
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* หัวข้อใหญ่แบบดุดัน */
    .sys-header { 
        font-size: 32px; 
        font-weight: 800; 
        color: #FFFFFF; 
        letter-spacing: -2px; 
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* กรอบข้อมูล */
    .terminal-box {
        border: 1px solid #333;
        padding: 15px;
        background: #0A0A0A;
        font-size: 12px;
        color: #00FF00; /* เขียว Terminal */
    }

    /* ปุ่มกดสไตล์เครื่องจักร */
    .stButton>button { 
        border: 1px solid #444; 
        color: #FFF; 
        background: #000; 
        border-radius: 0px; /* เหลี่ยมจัด */
        width: 100%; 
        height: 45px; 
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.2s;
    }
    .stButton>button:hover { 
        border-color: #FFF; 
        background: #111; 
        color: #FFF;
    }
    
    /* ซ่อน Decoration ของ Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. AUDIO ENGINE (CORE LOGIC)
# ---------------------------------------------------------
def create_waveform(freq, duration, type='sine'):
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), False)
    if type == 'sine':
        return np.sin(2 * np.pi * freq * t)
    elif type == 'square':
        return np.sign(np.sin(2 * np.pi * freq * t))
    elif type == 'saw':
        return 2 * (t * freq - np.floor(t * freq + 0.5))
    return np.zeros_like(t)

def generate_track(genre, duration=10):
    fs = 44100
    total_samples = int(fs * duration)
    output = np.zeros(total_samples)
    
    # PARAMETERS (ตั้งค่าตามแนวเพลง)
    bpm = 90
    kick_freq = 60
    
    if genre == "TRAP_HH": # Trap / HipHop
        bpm = 140
        kick_freq = 55
        pattern = [1, 0, 0, 0, 1, 0, 0, 0] # Kick pattern
        
    elif genre == "HEAVY_ROCK": # Rock
        bpm = 120
        kick_freq = 80
        pattern = [1, 0, 1, 0, 1, 0, 1, 0]
        
    elif genre == "SOUL_RB": # R&B
        bpm = 75
        kick_freq = 50
        pattern = [1, 0, 0, 0, 0, 0, 1, 0]
        
    else: # Default
        pattern = [1, 0, 0, 0]

    # BEAT GENERATION LOOP
    beat_len = int(fs * (60/bpm))
    current_pos = 0
    step = 0
    
    # สร้างเสียง Kick (เสียงเบสกระแทก)
    t_kick = np.linspace(0, 0.3, int(fs*0.3), False)
    kick_wave = np.sin(2*np.pi*kick_freq*t_kick) * np.exp(-10*t_kick)
    
    # สร้างเสียง Hihat (เสียงแหลม)
    noise = np.random.uniform(-0.5, 0.5, int(fs*0.05))
    hihat_wave = noise * np.exp(-30*np.linspace(0, 0.05, len(noise)))

    while current_pos < total_samples - fs:
        # ใส่ Kick ตาม Pattern
        if pattern[step % len(pattern)] == 1:
            end = min(current_pos + len(kick_wave), total_samples)
            output[current_pos:end] += kick_wave[:end-current_pos] * 0.8
            
        # ใส่ Hihat ทุกจังหวะ (Metronome)
        if step % 2 == 0:
            end = min(current_pos + len(hihat_wave), total_samples)
            output[current_pos:end] += hihat_wave[:end-current_pos] * 0.3

        current_pos += int(beat_len / 2) # ขยับทีละครึ่งจังหวะ
        step += 1

    # SYNTH LAYER (เสียงคอร์ด)
    t = np.linspace(0, duration, total_samples, False)
    if genre == "HEAVY_ROCK":
        # Distortion Bass
        synth = np.sign(np.sin(2*np.pi*55*t)) * 0.1
    elif genre == "TRAP_HH":
        # Sub Bass Sine
        synth = np.sin(2*np.pi*40*t) * 0.3
    else:
        # Smooth Chord
        synth = (np.sin(2*np.pi*261*t) + np.sin(2*np.pi*329*t)) * 0.1
        
    final_mix = output + synth
    
    # Normalize
    max_val = np.max(np.abs(final_mix))
    if max_val > 0: final_mix /= max_val
    
    # Export
    virtual_file = io.BytesIO()
    write(virtual_file, fs, (final_mix * 32767 * 0.8).astype(np.int16))
    return virtual_file, bpm

# ---------------------------------------------------------
# 3. INTERFACE (DISPLAY)
# ---------------------------------------------------------
st.markdown('<div class="sys-header">/// SYSTEM_AUDIO_GATEWAY_V.1</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.write("INPUT_PARAMETERS:")
    genre_input = st.selectbox("", ["TRAP_HH", "SOUL_RB", "HEAVY_ROCK"], label_visibility="collapsed")
    
    st.write("TIME_FRAME (SEC):")
    duration_input = st.slider("", 5, 20, 10, label_visibility="collapsed")
    
    st.markdown("---")
    
    # ปุ่มกดแบบดิบๆ
    if st.button("> EXECUTE_SEQUENCE"):
        with st.spinner("PROCESSING_WAVEFORMS..."):
            audio_data, bpm_out = generate_track(genre_input, duration_input)
            
            st.success("RENDER_COMPLETE.")
            
            # โชว์เครื่องเล่น
            st.markdown("OUTPUT_CHANNEL_01:")
            st.audio(audio_data, format='audio/wav')
            
            # เก็บค่าไว้แสดงผล Log
            st.session_state['log'] = f"""
            > TARGET: {genre_input}
            > BPM: {bpm_out}
            > BUFFER: {duration_input}s
            > STATUS: EXPORTED
            """

with col2:
    st.write("SYSTEM_LOG:")
    # ส่วนแสดงผลแบบ Code Terminal
    log_text = st.session_state.get('log', "> WAITING_FOR_COMMAND...")
    st.markdown(f"""
    <div class="terminal-box">
    ROOT@SERVER:~$ ./init_audio_engine<br>
    [OK] LIBRARIES LOADED<br>
    [OK] DRIVER: VIRTUAL_DAC<br>
    ---------------------------------<br>
    {log_text.replace(chr(10), '<br>')}
    <br>
    <span style="animation: blink 1s infinite;">_</span>
    </div>
    """, unsafe_allow_html=True)
    
    # กราฟิกคลื่นเสียงแบบเส้นเดียว (Minimal)
    st.write("")
    st.write("VISUAL_MONITOR:")
    chart_data = [random.random() for _ in range(50)]
    st.area_chart(chart_data, color="#333333")

