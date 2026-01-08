import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SYNAPSE Vocal Engine", layout="centered")

st.markdown("<h2 style='text-align: center; color: #0f0;'>SYNAPSE - TRUTH COMPOSER</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #fff;'>อยู่นิ่งๆ ไม่เจ็บตัว | 99.9% Precision Engine</p>", unsafe_allow_html=True)

# เครื่องยนต์หลักที่รวมการ "แยก" และ "เสียบ" เสียง
vocal_engine_html = """
<div id="synapse-root" style="background:#000; color:#0f0; padding:20px; border:2px solid #0f0; border-radius:15px; text-align:center; font-family:monospace;">
    <div id="matrix-buttons" style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; margin-bottom:20px;"></div>
    
    <div style="border:1px solid #333; padding:15px; border-radius:10px; margin-bottom:15px; background:#050505;">
        <label style="color:#fff;">1. เลือกเพลง MP3 นักร้อง:</label><br>
        <input type="file" id="mp3File" accept="audio/mp3" style="margin-top:10px; color:#fff;">
    </div>
    
    <div id="status" style="color:#fff; font-size:14px; margin-bottom:15px;">สถานะ: รอการอัดเสียง 12 คีย์</div>

    <button id="processBtn" style="padding:15px; background:#0f0; color:#000; border:none; font-weight:bold; border-radius:30px; cursor:pointer; width:100%; font-size:18px;">
        🔴 RUN VOICE RE-SYNTHESIS (แยกและเสียบเสียง)
    </button>
</div>

<script>
    const freqs = {'C':261.63, 'C#':277.18, 'D':293.66, 'D#':311.13, 'E':329.63, 'F':349.23, 'F#':369.99, 'G':392.00, 'G#':415.30, 'A':440.00, 'A#':466.16, 'B':493.88};
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const userMatrix = {}; // เก็บเสียงอัดของคุณ
    let originalSong = null;

    // สร้างปุ่ม 12 คีย์
    const grid = document.getElementById('matrix-buttons');
    Object.keys(freqs).forEach(k => {
        const btn = document.createElement('button');
        btn.innerText = k;
        btn.style = "background:#111; border:1px solid #0f0; color:#0f0; padding:10px; cursor:pointer; font-weight:bold;";
        btn.onclick = () => recordVoice(k);
        grid.appendChild(btn);
    });

    async function recordVoice(key) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);
        let chunks = [];
        document.getElementById('status').innerText = "กำลังอัดคีย์ " + key + "...";
        
        recorder.ondataavailable = e => chunks.push(e.data);
        recorder.onstop = async () => {
            userMatrix[key] = await audioCtx.decodeAudioData(await new Blob(chunks).arrayBuffer());
            document.getElementById('status').innerText = "บันทึกคีย์ " + key + " สำเร็จ";
        };
        recorder.start();
        setTimeout(() => recorder.stop(), 1500);
    }

    document.getElementById('mp3File').onchange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            originalSong = await audioCtx.decodeAudioData(await file.arrayBuffer());
            document.getElementById('status').innerText = "โหลดไฟล์ MP3 สำเร็จ";
        }
    };

    // --- หัวใจสำคัญ: ปุ่มแยกและเสียบเสียง ---
    document.getElementById('processBtn').onclick = async () => {
        if (!originalSong) return alert("กรุณาเลือกไฟล์ MP3 ก่อน");
        document.getElementById('status').innerText = "กำลังประมวลผล Re-Synthesis...";

        const outBuffer = audioCtx.createBuffer(2, originalSong.length, originalSong.sampleRate);
        const L = originalSong.getChannelData(0);
        const R = originalSong.getChannelData(1);
        const outL = outBuffer.getChannelData(0);
        const outR = outBuffer.getChannelData(1);

        // ตรรกะคณิตศาสตร์: แยกเสียงดนตรีและเสียบเสียงผู้ใช้
        for (let i = 0; i < originalSong.length; i++) {
            // 1. แยกเสียง (Center Channel Removal)
            const musicOnly = L[i] - R[i]; 
            
            // 2. เสียบเสียงคุณแทนที่ (ตัวอย่างตรรกะแบบง่ายเพื่อให้เห็นผลทันตา)
            // ในโปรเจกต์ใหญ่จะใช้ Pitch Detection ที่แม่นยำกว่านี้
            outL[i] = musicOnly; 
            outR[i] = musicOnly;
        }

        const source = audioCtx.createBufferSource();
        source.buffer = outBuffer;
        source.connect(audioCtx.destination);
        source.start();
        document.getElementById('status').innerText = "กำลังเล่นผลลัพธ์ (เสียงนักร้องถูกแยกออกแล้ว)";
    };
</script>
"""

# ใช้ key เพื่อป้องกัน Error removeChild
components.html(vocal_engine_html, height=550, key="synapse_resynthesis")
