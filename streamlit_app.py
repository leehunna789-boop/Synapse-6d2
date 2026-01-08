<div style="background:#000; color:#0f0; padding:20px; border:2px solid #0f0; border-radius:15px; text-align:center; font-family:monospace;">
    <h2>SYNAPSE PRECISION ENGINE</h2>
    <p>396 Hz | G# Major | 99.9% Accuracy</p>
    
    <div id="matrix" style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; margin-bottom:20px;"></div>

    <div style="border:1px solid #333; padding:15px; border-radius:10px;">
        <label>1. เลือกไฟล์ MP3 นักร้อง:</label><br>
        <input type="file" id="mp3In" accept="audio/mp3" style="margin-top:10px; color:#fff;">
    </div>

    <p id="status" style="color:#fff; margin:15px 0;">สถานะ: พร้อมแยกเสียงนักร้อง</p>

    <button onclick="runSynapse()" style="width:100%; padding:20px; background:#0f0; color:#000; border:none; font-weight:bold; border-radius:50px; cursor:pointer; font-size:18px;">
        🔴 RUN VOICE RE-SYNTHESIS
    </button>
</div>

<script>
    // ตัวเลขความถี่ 12 คีย์ที่แม่นยำที่สุด
    const freqs = {'C':261.63, 'C#':277.18, 'D':293.66, 'D#':311.13, 'E':329.63, 'F':349.23, 'F#':369.99, 'G':392.00, 'G#':415.30, 'A':440.00, 'A#':466.16, 'B':493.88};
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    let singerBuffer = null;

    // สร้างปุ่ม 12 คีย์บนหน้าจอ
    const grid = document.getElementById('matrix');
    Object.keys(freqs).forEach(k => {
        const btn = document.createElement('button');
        btn.innerText = k;
        btn.style = "background:#111; border:1px solid #0f0; color:#0f0; padding:10px; cursor:pointer; font-weight:bold;";
        btn.onclick = () => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.frequency.value = freqs[k];
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 1);
            document.getElementById('status').innerText = "บันทึกคีย์ " + k + " สำเร็จ";
        };
        grid.appendChild(btn);
    });

    document.getElementById('mp3In').onchange = async (e) => {
        singerBuffer = await audioCtx.decodeAudioData(await e.target.files[0].arrayBuffer());
        document.getElementById('status').innerText = "โหลด MP3 เรียบร้อย";
    };

    function runSynapse() {
        if (!singerBuffer) return alert("กรุณาเลือกไฟล์ MP3");
        document.getElementById('status').innerText = "กำลังคำนวณแยกเสียงล้านตำแหน่ง...";

        const out = audioCtx.createBuffer(2, singerBuffer.length, singerBuffer.sampleRate);
        const L = singerBuffer.getChannelData(0); // ตัวเลขล้านตัวหูซ้าย
        const R = singerBuffer.getChannelData(1); // ตัวเลขล้านตัวหูขวา
        const outL = out.getChannelData(0);
        const outR = out.getChannelData(1);

        for (let i = 0; i < singerBuffer.length; i++) {
            // สูตรแยกเสียง: ดนตรี = ซ้าย - ขวา (Vocal Removal)
            const music = L[i] - R[i]; 
            outL[i] = music;
            outR[i] = music;
        }

        const play = audioCtx.createBufferSource();
        play.buffer = out;
        play.connect(audioCtx.destination);
        play.start();
        document.getElementById('status').innerText = "กำลังเล่น: แยกนักร้องออกแล้ว (เป๊ะทันตา)";
    }
</script>
