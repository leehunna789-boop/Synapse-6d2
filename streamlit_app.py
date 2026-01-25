import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="Legendary MP3 Player", layout="wide")

# 2. ผ้าคลุมล่องหน (ซ่อนทุกอย่างขวาล่างให้กริบ)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none !important;}
            #stDecoration {display:none !important;}
            [data-testid="stStatusWidget"] {display:none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. ตัวเครื่องเล่นชุดเต็ม
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        :root { --neon: #00ff88; --bg: #050505; --border-width: 10px; }
        body { background-color: var(--bg); color: white; font-family: 'Orbitron', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .player-box {
            background: #111; border: var(--border-width) solid var(--neon);
            border-radius: 60px; padding: 40px; width: 350px; text-align: center;
            box-shadow: 0 0 50px rgba(0, 255, 136, 0.2);
        }
        .knob-container { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; background: #1a1a1a; padding: 15px; border-radius: 25px; }
        .btn-main { background: var(--neon); border: none; width: 75px; height: 75px; border-radius: 50%; font-size: 2rem; cursor: pointer; box-shadow: 0 0 20px var(--neon); }
        .slider { width: 100%; accent-color: var(--neon); cursor: pointer; }
        .playlist { margin-top: 20px; max-height: 100px; overflow-y: auto; font-size: 0.8rem; text-align: left; border-top: 1px solid #333; }
    </style>
</head>
<body>
    <div class="player-box">
        <h2 style="color:var(--neon); margin-bottom:5px;">เสียง...</h2>
        <div id="trackName" style="font-size:0.8rem; margin-bottom:15px; color:#888;">ยังไม่มีเพลง...</div>
        
        <div class="knob-container">
            <div><small style="color:var(--neon)">BASS</small><input type="range" id="bass" class="slider" min="0" max="20" value="0"></div>
            <div><small style="color:var(--neon)">MIX</small><input type="range" id="gain" class="slider" min="0" max="2" step="0.1" value="1"></div>
        </div>

        <input type="range" id="progress" class="slider" value="0">
        
        <div style="display:flex; justify-content: space-around; align-items: center; margin: 15px 0;">
            <button onclick="prev()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">⏮</button>
            <button id="playBtn" class="btn-main" onclick="toggle()">▶</button>
            <button onclick="next()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">⏭</button>
        </div>

        <label style="display: block; cursor: pointer; color: var(--neon); font-size:0.9rem; border: 1px dashed var(--neon); padding: 10px; border-radius: 15px;">
            <input type="file" id="files" multiple accept="audio/*" style="display:none;">
            [ + เลือกเพลงเข้าเครื่อง ]
        </label>
        <div id="list" class="playlist"></div>
    </div>

    <audio id="audio"></audio>

    <script>
        const audio = document.getElementById('audio');
        let songs = []; let current = 0;
        let audioCtx, bassNode, gainNode, source;

        function init() {
            if (audioCtx) return;
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            bassNode = audioCtx.createBiquadFilter();
            bassNode.type = "lowshelf"; bassNode.frequency.value = 200;
            gainNode = audioCtx.createGain();
            source = audioCtx.createMediaElementSource(audio);
            source.connect(bassNode).connect(gainNode).connect(audioCtx.destination);
        }

        document.getElementById('files').onchange = (e) => {
            init();
            const f = Array.from(e.target.files);
            f.forEach(file => songs.push({name: file.name, url: URL.createObjectURL(file)}));
            if(!audio.src) load(0);
            updateList();
        };

        function load(i) {
            current = i; audio.src = songs[i].url;
            document.getElementById('trackName').innerText = songs[i].name;
            play();
        }

        function toggle() { audio.paused ? play() : pause(); }
        function play() { if(audioCtx.state==='suspended') audioCtx.resume(); audio.play(); document.getElementById('playBtn').innerText='⏸'; }
        function pause() { audio.pause(); document.getElementById('playBtn').innerText='▶'; }
        function next() { if(songs.length) load((current+1)%songs.length); }
        function prev() { if(songs.length) load((current-1+songs.length)%songs.length); }

        function updateList() {
            document.getElementById('list').innerHTML = songs.map((s,i) => 
                `<div onclick="load(${i})" style="padding:5px; color:${i===current?var(--neon):'#666'}">${i+1}. ${s.name}</div>`
            ).join('');
        }

        document.getElementById('bass').oninput = (e) => bassNode.gain.value = e.target.value;
        document.getElementById('gain').oninput = (e) => gainNode.gain.value = e.target.value;
        audio.ontimeupdate = () => { document.getElementById('progress').max = audio.duration; document.getElementById('progress').value = audio.currentTime; };
        document.getElementById('progress').oninput = (e) => audio.currentTime = e.target.value;
        audio.onended = next;
    </script>
</body>
</html>
"""

components.html(html_code, height=800)
