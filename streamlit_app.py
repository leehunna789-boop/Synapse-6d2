import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Legendary MP3 Player", layout="wide")

# ส่วนซ่อนปุ่ม Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    #stDecoration {display:none !important;}
    [data-testid="stStatusWidget"] {display:none !important;}
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <style>
        :root { --neon: #00ff88; --bg: #050505; --border-width: 10px; }
        body { background: var(--bg); color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .player-box {
            background: #111; border: var(--border-width) solid var(--neon);
            border-radius: 50px; padding: 40px; width: 320px; text-align: center;
            box-shadow: 0 0 50px rgba(0, 255, 136, 0.2);
        }
        .knob-container { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; background: #1a1a1a; padding: 15px; border-radius: 25px; }
        .btn-main { background: var(--neon); border: none; width: 80px; height: 80px; border-radius: 50%; font-size: 2.5rem; cursor: pointer; box-shadow: 0 0 20px var(--neon); }
        .slider { width: 100%; accent-color: var(--neon); cursor: pointer; }
        .playlist { margin-top: 20px; max-height: 120px; overflow-y: auto; text-align: left; font-size: 0.85rem; border-top: 1px solid #333; padding-top: 10px; }
        .song-item { padding: 8px; cursor: pointer; border-radius: 5px; margin-bottom: 2px; }
        .song-item:hover { background: #222; }
    </style>
</head>
<body>
    <div class="player-box">
        <h2 style="color:var(--neon); margin:0;">MUSIC.อยู่นิ้งๆไม่เจ็บตัว...</h2>
        <div id="trackName" style="font-size:0.9rem; margin:15px 0; color:#aaa; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">รอเลือกเพลง...</div>
        
        <div class="knob-container">
            <div><small style="color:var(--neon)">BASS</small><input type="range" id="bass" class="slider" min="0" max="20" value="0"></div>
            <div><small style="color:var(--neon)">MIX</small><input type="range" id="gain" class="slider" min="0" max="2" step="0.1" value="1"></div>
        </div>

        <input type="range" id="progress" class="slider" value="0">
        
        <div style="display:flex; justify-content: space-around; align-items: center; margin: 20px 0;">
            <button onclick="prev()" style="background:none; border:none; color:white; font-size:1.8rem; cursor:pointer;">⏮</button>
            <button id="playBtn" class="btn-main" onclick="toggle()">▶</button>
            <button onclick="next()" style="background:none; border:none; color:white; font-size:1.8rem; cursor:pointer;">⏭</button>
        </div>

        <label style="display: block; cursor: pointer; color: var(--neon); font-weight:bold; border: 2px solid var(--neon); padding: 12px; border-radius: 20px;">
            <input type="file" id="files" multiple accept="audio/*" style="display:none;">
            [ + อัปโหลดเพลง ]
        </label>
        
        <div id="list" class="playlist"></div>
    </div>

    <audio id="audioTag"></audio>

    <script>
        const audio = document.getElementById('audioTag');
        const playBtn = document.getElementById('playBtn');
        const trackNameDisp = document.getElementById('trackName');
        const listDisp = document.getElementById('list');
        
        let songs = [];
        let currentIdx = 0;
        let audioCtx, bassNode, gainNode, source;

        function initAudio() {
            if (audioCtx) return;
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            bassNode = audioCtx.createBiquadFilter();
            bassNode.type = "lowshelf";
            bassNode.frequency.value = 200;
            gainNode = audioCtx.createGain();
            source = audioCtx.createMediaElementSource(audio);
            source.connect(bassNode).connect(gainNode).connect(audioCtx.destination);
        }

        document.getElementById('files').onchange = (e) => {
            initAudio();
            const f = Array.from(e.target.files);
            f.forEach(file => {
                songs.push({ name: file.name, url: URL.createObjectURL(file) });
            });
            if (songs.length > 0 && !audio.src) {
                loadSong(0);
            }
            updatePlaylistUI();
        };

        function loadSong(index) {
            currentIdx = index;
            audio.src = songs[index].url;
            trackNameDisp.innerText = songs[index].name;
            updatePlaylistUI();
            playAudio();
        }

        function toggle() {
            if (!audio.src) return;
            audio.paused ? playAudio() : pauseAudio();
        }

        function playAudio() {
            if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
            audio.play();
            playBtn.innerText = '⏸';
        }

        function pauseAudio() {
            audio.pause();
            playBtn.innerText = '▶';
        }

        function next() {
            if (songs.length === 0) return;
            loadSong((currentIdx + 1) % songs.length);
        }

        function prev() {
            if (songs.length === 0) return;
            loadSong((currentIdx - 1 + songs.length) % songs.length);
        }

        function updatePlaylistUI() {
            listDisp.innerHTML = songs.map((s, i) => `
                <div class="song-item" onclick="loadSong(${i})" style="color: ${i === currentIdx ? '#00ff88' : '#888'}">
                    ${i + 1}. ${s.name}
                </div>
            `).join('');
        }

        // ปรับแต่งเสียง
        document.getElementById('bass').oninput = (e) => { if(bassNode) bassNode.gain.value = e.target.value; };
        document.getElementById('gain').oninput = (e) => { if(gainNode) gainNode.gain.value = e.target.value; };
        
        // Progress Bar
        audio.ontimeupdate = () => {
            const prog = document.getElementById('progress');
            prog.max = audio.duration || 0;
            prog.value = audio.currentTime;
        };
        document.getElementById('progress').oninput = (e) => {
            audio.currentTime = e.target.value;
        };
        audio.onended = next;
    </script>
</body>
</html>
"""

components.html(html_code, height=850)
