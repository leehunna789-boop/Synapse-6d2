import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Legendary MP3 Player", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <style>
        :root { 
            --neon: #00ff88; 
            --bg: #050505;
        }
        
        body { 
            background-color: var(--bg);
            color: white; font-family: 'Orbitron', sans-serif;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; margin: 0; overflow: hidden;
        }

        /* เอฟเฟกต์พื้นหลังเรืองแสง */
        .bg-glow {
            position: fixed; top: 50%; left: 50%; width: 500px; height: 500px;
            background: radial-gradient(circle, var(--neon) 0%, transparent 70%);
            opacity: 0.1; transform: translate(-50%, -50%); z-index: -1;
            filter: blur(80px); transition: 0.5s;
        }

        .player-box {
            background: rgba(20, 20, 20, 0.8);
            border: 2px solid var(--neon);
            border-radius: 50px;
            padding: 40px;
            width: 350px;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
            backdrop-filter: blur(10px);
        }

        .visual-circle {
            width: 220px; height: 220px;
            border-radius: 50%; margin: 0 auto 30px;
            border: 4px dashed var(--neon);
            display: flex; justify-content: center; align-items: center;
            position: relative; transition: 0.5s;
        }

        .visual-circle.active { animation: pulse 1.5s infinite; }

        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 0px var(--neon); }
            50% { transform: scale(1.05); box-shadow: 0 0 20px var(--neon); }
            100% { transform: scale(1); box-shadow: 0 0 0px var(--neon); }
        }

        #title { font-size: 1.1rem; letter-spacing: 2px; margin-bottom: 20px; color: var(--neon); height: 50px; overflow: hidden; }

        .btn-main {
            background: var(--neon); color: black; border: none;
            width: 70px; height: 70px; border-radius: 50%;
            font-size: 2rem; cursor: pointer; font-weight: bold;
            box-shadow: 0 0 20px var(--neon); transition: 0.3s;
        }
        .btn-main:hover { transform: translateY(-5px); box-shadow: 0 0 40px var(--neon); }

        .slider { width: 100%; margin: 20px 0; accent-color: var(--neon); }

        .controls-row { display: flex; justify-content: space-around; align-items: center; margin-top: 20px; }
        
        .side-btn { background: none; border: 1px solid var(--neon); color: var(--neon); padding: 10px; border-radius: 10px; cursor: pointer; }

        .playlist-area {
            margin-top: 30px; max-height: 120px; overflow-y: auto;
            border-top: 1px solid #333; padding-top: 10px; font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="bg-glow" id="glow"></div>
    
    <div class="player-box">
        <div class="visual-circle" id="circle">
            <span style="font-size: 5rem;">🎵</span>
        </div>
        
        <div id="title">เลือกเพลงเพื่อเริ่มความเท่...</div>
        
        <input type="range" id="progress" class="slider" value="0">
        
        <div class="controls-row">
            <button class="side-btn" onclick="prev()">PREV</button>
            <button id="playBtn" class="btn-main" onclick="toggle()">▶</button>
            <button class="side-btn" onclick="next()">NEXT</button>
        </div>

        <div style="margin-top: 20px;">
            <input type="range" id="vol" class="slider" min="0" max="1" step="0.1" value="0.7">
        </div>

        <label style="display: block; margin-top: 20px; cursor: pointer; color: var(--neon); border: 1px solid var(--neon); padding: 10px; border-radius: 20px;">
            <input type="file" id="files" multiple accept="audio/*" style="display:none;">
            [ + อัปโหลดเพลง ]
        </label>

        <div id="list" class="playlist-area"></div>
    </div>

    <audio id="player"></audio>

    <script>
        const audio = document.getElementById('player');
        const playBtn = document.getElementById('playBtn');
        const circle = document.getElementById('circle');
        const glow = document.getElementById('glow');
        let songs = [];
        let current = 0;

        document.getElementById('files').onchange = (e) => {
            const f = Array.from(e.target.files);
            f.forEach(file => songs.push({name: file.name, url: URL.createObjectURL(file)}));
            updateList();
            if(!audio.src) load(0);
        };

        function load(i) {
            current = i;
            audio.src = songs[i].url;
            document.getElementById('title').innerText = songs[i].name;
            updateList();
            play();
        }

        function toggle() { audio.paused ? play() : pause(); }

        function play() { 
            audio.play(); 
            playBtn.innerText = '⏸'; 
            circle.classList.add('active');
            glow.style.opacity = "0.3";
        }

        function pause() { 
            audio.pause(); 
            playBtn.innerText = '▶'; 
            circle.classList.remove('active');
            glow.style.opacity = "0.1";
        }

        function next() { if(songs.length) load((current+1)%songs.length); }
        function prev() { if(songs.length) load((current-1+songs.length)%songs.length); }

        function updateList() {
            document.getElementById('list').innerHTML = songs.map((s,i) => 
                `<div onclick="parent.playSong(${i})" style="padding:8px; cursor:pointer; color:${i===current?'#00ff88':'#666'}">${i+1}. ${s.name}</div>`
            ).join('');
        }
        window.playSong = load;

        audio.ontimeupdate = () => {
            document.getElementById('progress').max = audio.duration;
            document.getElementById('progress').value = audio.currentTime;
        };
        document.getElementById('progress').oninput = (e) => audio.currentTime = e.target.value;
        document.getElementById('vol').oninput = (e) => audio.volume = e.target.value;
        audio.onended = next;
    </script>
</body>
</html>
"""

st.markdown("<h1 style='text-align: center;'>⚡ MP3 THE LEGEND</h1>", unsafe_allow_html=True)
components.html(html_code, height=750)
