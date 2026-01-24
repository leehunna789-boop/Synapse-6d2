import streamlit as st
import streamlit.components.v1 as components
import streamlit as st

# --- วางแทนที่ของเดิมได้เลยครับ ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none !important;}
            #stDecoration {display:none !important;}
            [data-testid="stStatusWidget"] {display:none !important;}
            footer {display:none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)     """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.set_page_config(page_title="Heavy Metal MP3 Player", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <style>
        :root { 
            --neon: #00ff88; 
            --bg: #0a0a0a;
            --border-width: 8px; /* ปรับความหนาขอบตรงนี้ครับลูกพี่ */
        }
        
        body { 
            background-color: var(--bg);
            color: white; font-family: 'Orbitron', sans-serif;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; margin: 0;
        }

        .player-box {
            background: #151515;
            /* ขอบใหญ่หนาตามสั่ง */
            border: var(--border-width) solid var(--neon);
            border-radius: 60px;
            padding: 45px;
            width: 380px;
            text-align: center;
            box-shadow: 0 0 50px rgba(0, 255, 136, 0.3), inset 0 0 20px rgba(0, 255, 136, 0.1);
        }

        .visual-circle {
            width: 180px; height: 180px;
            border-radius: 50%; margin: 0 auto 25px;
            border: 10px solid #222;
            border-top-color: var(--neon);
            animation: spin 2s linear infinite;
            animation-play-state: paused;
        }
        .visual-circle.active { animation-play-state: running; }

        @keyframes spin { 100% { transform: rotate(360deg); } }

        .knob-container {
            display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
            margin: 25px 0; background: #222; padding: 20px; border-radius: 30px;
            border: 3px solid #333;
        }

        .knob-label { font-size: 0.7rem; color: var(--neon); margin-bottom: 5px; display: block; }

        .btn-main {
            background: var(--neon); color: black; border: none;
            width: 80px; height: 80px; border-radius: 50%;
            font-size: 2.2rem; cursor: pointer; font-weight: bold;
            box-shadow: 0 0 30px var(--neon);
        }

        .slider { width: 100%; accent-color: var(--neon); cursor: pointer; }

        .playlist-area {
            margin-top: 25px; max-height: 100px; overflow-y: auto;
            text-align: left; font-size: 0.8rem; border-top: 2px solid #333;
        }
    </style>
</head>
<body>
    <div class="player-box">
        <div class="visual-circle" id="circle"></div>
        <div id="title" style="color:var(--neon); margin-bottom:10px; height:40px;">เตรียมระเบิดพลังเสียง...</div>

        <div class="knob-container">
            <div>
                <span class="knob-label">🔊 BASS BOOST</span>
                <input type="range" id="bassBoost" class="slider" min="0" max="10" value="0">
            </div>
            <div>
                <span class="knob-label">🎚️ MIX GAIN</span>
                <input type="range" id="mixGain" class="slider" min="0" max="2" step="0.1" value="1">
            </div>
        </div>

        <input type="range" id="progress" class="slider" value="0">
        
        <div style="display:flex; justify-content: space-around; align-items: center; margin: 20px 0;">
            <button onclick="prev()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">⏮</button>
            <button id="playBtn" class="btn-main" onclick="toggle()">▶</button>
            <button onclick="next()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">⏭</button>
        </div>

        <label style="display: block; cursor: pointer; color: var(--neon); font-weight:bold;">
            <input type="file" id="files" multiple accept="audio/*" style="display:none;">
            [ + ใส่แผ่นเพลง ]
        </label>

        <div id="list" class="playlist-area"></div>
    </div>

    <audio id="player1"></audio>
    <audio id="player2"></audio>

    <script>
        let songs = [];
        let current = 0;
        let audioCtx, bassNode, gainNode, source1, source2;
        let currentPlayer = document.getElementById('player1');

        function initAudio(player) {
            if (audioCtx) return;
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            gainNode = audioCtx.createGain();
            bassNode = audioCtx.createBiquadFilter();
            bassNode.type = "lowshelf";
            bassNode.frequency.value = 200;

            source1 = audioCtx.createMediaElementSource(document.getElementById('player1'));
            source2 = audioCtx.createMediaElementSource(document.getElementById('player2'));

            source1.connect(bassNode);
            source2.connect(bassNode);
            bassNode.connect(gainNode);
            gainNode.connect(audioCtx.destination);
        }

        document.getElementById('files').onchange = (e) => {
            initAudio();
            const f = Array.from(e.target.files);
            f.forEach(file => songs.push({name: file.name, url: URL.createObjectURL(file)}));
            updateList();
            if(!currentPlayer.src) load(0);
        };

        function load(i) {
            current = i;
            currentPlayer.src = songs[i].url;
            document.getElementById('title').innerText = songs[i].name;
            updateList();
            play();
        }

        function play() { 
            if(audioCtx.state === 'suspended') audioCtx.resume();
            currentPlayer.play(); 
            document.getElementById('playBtn').innerText = '⏸';
            document.getElementById('circle').classList.add('active');
        }

        function toggle() { currentPlayer.paused ? play() : pause(); }
        function pause() { currentPlayer.pause(); document.getElementById('playBtn').innerText = '▶'; document.getElementById('circle').classList.remove('active');}

        // ระบบ Crossfade: เพลงต่อไปจะค่อยๆ ดังขึ้นก่อนเพลงเก่าจบ 10 วินาที
        function checkCrossfade() {
            if (currentPlayer.duration - currentPlayer.currentTime < 5 && songs.length > 1) {
                let nextIdx = (current + 1) % songs.length;
                let nextPlayer = currentPlayer.id === 'player1' ? document.getElementById('player2') : document.getElementById('player1');
                
                if (nextPlayer.paused) {
                    nextPlayer.src = songs[nextIdx].url;
                    nextPlayer.volume = 0;
                    nextPlayer.play();
                    
                    // ค่อยๆ สลับเสียง
                    let fadeTime = 5000; 
                    let interval = 100;
                    let step = interval / fadeTime;
                    
                    let fade = setInterval(() => {
                        if (currentPlayer.volume > 0.1) currentPlayer.volume -= step;
                        if (nextPlayer.volume < 0.9) nextPlayer.volume += step;
                        else {
                            clearInterval(fade);
                            currentPlayer.pause();
                            currentPlayer = nextPlayer;
                            current = nextIdx;
                            document.getElementById('title').innerText = songs[current].name;
                            updateList();
                        }
                    }, interval);
                }
            }
        }

        setInterval(() => { if(!currentPlayer.paused) checkCrossfade(); }, 1000);

        function next() { if(songs.length) load((current+1)%songs.length); }
        function prev() { if(songs.length) load((current-1+songs.length)%songs.length); }

        function updateList() {
            document.getElementById('list').innerHTML = songs.map((s,i) => 
                `<div onclick="parent.playSong(${i})" style="padding:8px; cursor:pointer; color:${i===current?'#00ff88':'#666'}">${i+1}. ${s.name}</div>`
            ).join('');
        }
        window.playSong = load;

        // ปรับ Bass และ Mix ตาม Slider
        document.getElementById('bassBoost').oninput = (e) => bassNode.gain.value = e.target.value;
        document.getElementById('mixGain').oninput = (e) => gainNode.gain.value = e.target.value;
        
        currentPlayer.ontimeupdate = () => {
            document.getElementById('progress').max = currentPlayer.duration;
            document.getElementById('progress').value = currentPlayer.currentTime;
        };
    </script>
</body>
</html>
"""

st.markdown("<h1 style='text-align: center; color: #00ff88;'>🦾 MP3.PLAYER.MUSIC.อยู่นิ้งๆไม่เจ็บตัว</h1>", unsafe_allow_html=True)
components.html(html_code, height=800)
