import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pro Music Player", layout="centered")

# โค้ด HTML/JS/CSS เวอร์ชั่นอัปเกรด
html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <style>
        :root { 
            --primary-color: #2ecc71; 
            --bg-color: #1a1a1a; 
            --card-bg: #2d2d2d; 
            --text-color: #ffffff; 
            --neon-shadow: 0 0 10px #2ecc71;
        }
        body { font-family: sans-serif; background-color: var(--bg-color); color: var(--text-color); display: flex; justify-content: center; align-items: center; min-height: 95vh; margin: 0; transition: 0.3s; }
        .player-card { background: var(--card-bg); padding: 25px; border-radius: 30px; width: 340px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.7); border: 1px solid #444; }
        
        /* ปุ่มและไฟ */
        .controls button { background: none; border: none; color: white; cursor: pointer; font-size: 1.8rem; margin: 0 10px; transition: 0.2s; text-shadow: var(--neon-shadow); }
        .controls button:hover { transform: scale(1.2); color: var(--primary-color); }
        
        input[type="range"] { width: 100%; accent-color: var(--primary-color); cursor: pointer; }
        
        .eq-section { margin-top: 20px; background: #222; padding: 10px; border-radius: 15px; font-size: 0.8rem; }
        .eq-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 5px; }

        .playlist { text-align: left; max-height: 120px; overflow-y: auto; margin-top: 15px; border-top: 1px solid #444; padding-top: 10px; font-size: 0.85rem; }
        
        .btn-action { display: inline-block; padding: 8px 15px; background: var(--primary-color); border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 0.8rem; margin: 5px; border: none; color: black; box-shadow: var(--neon-shadow); }
        
        .theme-selector { margin-top: 15px; display: flex; justify-content: center; gap: 10px; }
        .dot { height: 15px; width: 15px; border-radius: 50%; cursor: pointer; border: 2px solid white; }
    </style>
</head>
<body>
    <div class="player-card">
        <h3 style="margin-top:0;">🎧 Music Pro Max</h3>
        <p id="title" style="color: var(--primary-color); font-weight:bold;">กรุณาเพิ่มเพลง...</p>
        
        <input type="range" id="progressBar" value="0">
        
        <div class="controls">
            <button onclick="prevTrack()">⏮</button>
            <button id="playPauseBtn" onclick="togglePlay()">▶️</button>
            <button onclick="nextTrack()">⏭</button>
        </div>

        <div class="eq-section">
            <span>🎚️ ปรับแต่งเสียง (Equalizer)</span>
            <div class="eq-grid">
                <div>Bass: <input type="range" id="bassGain" min="-10" max="10" value="0"></div>
                <div>Treble: <input type="range" id="trebleGain" min="-10" max="10" value="0"></div>
            </div>
        </div>

        <div style="margin-top:15px;">
            <span>🔊</span> <input type="range" id="volumeControl" min="0" max="1" step="0.1" value="0.8" style="width: 80%;">
        </div>

        <div class="theme-selector">
            <span>เปลี่ยนสีไฟ:</span>
            <div class="dot" style="background:#2ecc71" onclick="changeTheme('#2ecc71')"></div>
            <div class="dot" style="background:#e74c3c" onclick="changeTheme('#e74c3c')"></div>
            <div class="dot" style="background:#3498db" onclick="changeTheme('#3498db')"></div>
            <div class="dot" style="background:#f1c40f" onclick="changeTheme('#f1c40f')"></div>
        </div>

        <div style="margin-top:15px;">
            <label class="btn-action">
                <input type="file" id="fileInput" multiple accept="audio/*" style="display:none;">
                📂 เพิ่มเพลง
            </label>
        </div>

        <div id="playlist" class="playlist"></div>
    </div>

    <audio id="audioPlayer" crossOrigin="anonymous"></audio>

    <script>
        const audio = document.getElementById('audioPlayer');
        const playPauseBtn = document.getElementById('playPauseBtn');
        const fileInput = document.getElementById('fileInput');
        const playlistDisplay = document.getElementById('playlist');
        const title = document.getElementById('title');
        const progressBar = document.getElementById('progressBar');

        let songs = [];
        let currentSongIndex = 0;
        let audioCtx, bassFilter, trebleFilter, source;

        // ระบบ Equalizer
        function initAudioContext() {
            if (audioCtx) return;
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            source = audioCtx.createMediaElementSource(audio);
            
            bassFilter = audioCtx.createBiquadFilter();
            bassFilter.type = "lowshelf";
            bassFilter.frequency.value = 200;

            trebleFilter = audioCtx.createBiquadFilter();
            trebleFilter.type = "highshelf";
            trebleFilter.frequency.value = 3000;

            source.connect(bassFilter);
            bassFilter.connect(trebleFilter);
            trebleFilter.connect(audioCtx.destination);
        }

        document.getElementById('bassGain').addEventListener('input', (e) => {
            if(bassFilter) bassFilter.gain.value = e.target.value;
        });
        document.getElementById('trebleGain').addEventListener('input', (e) => {
            if(trebleFilter) trebleFilter.gain.value = e.target.value;
        });

        // เปลี่ยนสีไฟปุ่ม
        function changeTheme(color) {
            document.documentElement.style.setProperty('--primary-color', color);
            document.documentElement.style.setProperty('--neon-shadow', `0 0 15px ${color}`);
            updatePlaylist();
        }

        fileInput.addEventListener('change', (e) => {
            initAudioContext();
            const files = Array.from(e.target.files);
            files.forEach(file => {
                songs.push({ name: file.name, url: URL.createObjectURL(file) });
            });
            updatePlaylist();
            if (songs.length > 0 && !audio.src) loadSong(0);
        });

        function updatePlaylist() {
            const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color');
            playlistDisplay.innerHTML = songs.map((s, i) => 
                `<div style="padding:5px; cursor:pointer; color:${i===currentSongIndex?primaryColor:'white'}" onclick="parent.loadSongFromJS(${i})">${i+1}. ${s.name}</div>`
            ).join('');
        }

        window.loadSongFromJS = (index) => loadSong(index);

        function loadSong(index) {
            currentSongIndex = index;
            audio.src = songs[index].url;
            title.innerText = songs[index].name;
            audio.play();
            playPauseBtn.innerText = '⏸';
            updatePlaylist();
        }

        function togglePlay() {
            if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
            if (audio.paused) { audio.play(); playPauseBtn.innerText = '⏸'; }
            else { audio.pause(); playPauseBtn.innerText = '▶️'; }
        }

        function nextTrack() { if(songs.length) loadSong((currentSongIndex + 1) % songs.length); }
        function prevTrack() { if(songs.length) loadSong((currentSongIndex - 1 + songs.length) % songs.length); }

        audio.addEventListener('ended', nextTrack);
        audio.addEventListener('timeupdate', () => { progressBar.max = audio.duration; progressBar.value = audio.currentTime; });
        progressBar.addEventListener('input', () => audio.currentTime = progressBar.value);
        document.getElementById('volumeControl').addEventListener('input', (e) => audio.volume = e.target.value);
    </script>
</body>
</html>
"""

st.title("🎧 MP3 Player : อยู่นิ้งๆไม่เจ็บตัว Edition")
st.write("เพิ่มเพลง ปรับเบส เปลี่ยนสีไฟ ได้ครบในแอปเดียว!")

components.html(html_code, height=650)
