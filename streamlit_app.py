import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าพื้นฐาน (คงความเป็นมืออาชีพของ SYNAPSE)
st.set_page_config(page_title="SYNAPSE Blueprint", layout="centered")

# 2. หัวข้อแอปตามโลโก้ของคุณ
st.markdown("<h1 style='text-align: center; color: #0f0;'>SYNAPSE ENGINE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #fff;'>396 Hz | G# Major | 99.9% Accuracy</p>", unsafe_allow_html=True)

# 3. โค้ดเครื่องยนต์หลัก (ปรับปรุงเพื่อไม่ให้เกิด removeChild Error)
vocal_engine_html = """
<div id="synapse-app" style="background:#000; color:#0f0; padding:20px; border:2px solid #0f0; border-radius:15px; text-align:center; font-family:monospace;">
    <div id="matrix-display" style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; margin-bottom:20px;">
        </div>
    
    <div style="border:1px solid #333; padding:15px; border-radius:10px; margin-bottom:15px;">
        <label>UPLOAD MP3 (นักร้องต้นฉบับ):</label><br>
        <input type="file" id="mp3File" accept="audio/mp3" style="margin-top:10px; color:#fff;">
    </div>
    
    <div id="status" style="color:#fff; font-size:12px; margin-bottom:15px;">สถานะ: ระบบพร้อม (Offline Mode)</div>

    <button id="runResynthesis" style="padding:15px 30px; background:#0f0; color:#000; border:none; font-weight:bold; border-radius:30px; cursor:pointer; width:100%;">
        🔴 RUN VOICE RE-SYNTHESIS
    </button>
</div>

<script>
    // ฐานข้อมูลความถี่ 12 คีย์ของคุณ
    const freqMap = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
        'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
        'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
    };

    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    // สร้างปุ่มคีย์ลงใน Matrix Grid
    const grid = document.getElementById('matrix-display');
    Object.keys(freqMap).forEach(k => {
        const btn = document.createElement('button');
        btn.innerText = k;
        btn.style = "background:#111; border:1px solid #0f0; color:#0f0; padding:10px; cursor:pointer; font-weight:bold;";
        btn.onclick = () => {
            playTone(freqMap[k]);
            document.getElementById('status').innerText = "กำลังฟังคีย์ " + k + "...";
        };
        grid.appendChild(btn);
    });

    function playTone(f) {
        const o = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        o.type = 'sine'; o.frequency.value = f;
        g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1);
        o.connect(g); g.connect(audioCtx.destination);
        o.start(); o.stop(audioCtx.currentTime + 1);
    }
</script>
"""

# 4. แสดงผลโดยใช้ 'key' เพื่อป้องกันการ Error
components.html(vocal_engine_html, height=550, key="synapse_v1")

st.markdown("<p style='text-align: center; color: #555;'>STAY STILL & HEAL</p>", unsafe_allow_html=True)
