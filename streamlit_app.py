import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าจอ Streamlit เล็กน้อย
st.set_page_config(page_title="My Music Player", layout="centered")

# 1. นำโค้ด HTML/CSS/JS ทั้งหมดมาใส่ในตัวแปร html_code (ใช้เครื่องหมายคำพูด 3 อัน """ เพื่อคลุมทั้งหมด)
html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <style>
        :root { --primary-color: #2ecc71; --bg-color: #1a1a1a; --card-bg: #2d2d2d; --text-color: #ffffff; }
        body { font-family: sans-serif; background-color: var(--bg-color); color: var(--text-color); display: flex; justify-content: center; align-items: center; min-height: 90vh; margin: 0; }
        .player-card { background: var(--card-bg); padding: 20px; border-radius: 20px; width: 320px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .controls button { background: none; border: none; color: white; cursor: pointer; font-size: 1.5rem; margin: 0 10px; }
        input[type="range"] { width: 100%; accent-color: var(--primary-color); }
        .playlist { text-align: left; max-height: 150px; overflow-y: auto; margin-top: 15px; border-top: 1px solid #444; }
        .custom-file-upload { display: inline-block; padding: 8px 20px; background: var(--primary-color); border-radius: 20px; cursor: pointer; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="player-card">
        <h3>🎵 My Player</h3>
        <p id="title">ยังไม่มีเพลง</p>
        <input type="range" id="progressBar" value="0">
        <div class="controls">
            <button onclick="prevTrack()">⏮</button>
            <button id="playPauseBtn" onclick="togglePlay()">▶️</button>
            <button onclick="nextTrack()">⏭</button>
        </div>
        <input type="range" id="volumeControl" min="0" max="1" step="0.1" value="1">
        <label class="custom-file-upload">
            <input type="file" id="fileInput" multiple accept="audio/*" style="display:none;">
            เพิ่มเพลง
        </label>
        <div id="playlist" class="playlist"></div>
    </div>

    <audio id="audioPlayer"></audio>

    <script>
        const audio = document.getElementById('audioPlayer');
        const playPauseBtn = document.getElementById('playPauseBtn');
        const fileInput = document.getElementById('fileInput');
        const playlistDisplay = document.getElementById('playlist');
        const title = document.getElementById('title');
        const progressBar = document.getElementById('progressBar');

        let songs = [];
        let currentSongIndex = 0;

        fileInput.addEventListener('change', (e) => {
            const files = Array.from(e.target.files);
            files.forEach(file => {
                songs.push({ name: file.name, url: URL.createObjectURL(file) });
            });
            updatePlaylist();
            if (songs.length > 0 && !audio.src) loadSong(0);
        });

        function updatePlaylist() {
            playlistDisplay.innerHTML = songs.map((s, i) => 
                `<div style="padding:5px; cursor:pointer; color:${i===currentSongIndex?'#2ecc71':'white'}" onclick="parent.loadSongFromJS(${i})">${i+1}. ${s.name}</div>`
            ).join('');
        }

        // ฟังชั่นเสริมสำหรับการคลิกในลิสต์ (ปรับให้เข้ากับ iframe)
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
            if (audio.paused) { audio.play(); playPauseBtn.innerText = '⏸'; }
            else { audio.pause(); playPauseBtn.innerText = '▶️'; }
        }

        function nextTrack() { if(songs.length) loadSong((currentSongIndex + 1) % songs.length); }
        function prevTrack() { if(songs.length) loadSong((currentSongIndex - 1 + songs.length) % songs.length); }

        audio.addEventListener('ended', nextTrack);
        audio.addEventListener('timeupdate', () => { progressBar.max = audio.duration; progressBar.value = audio.currentTime; });
        progressBar.addEventListener('input', () => audio.currentTime = progressBar.value);
    </script>
</body>
</html>
"""

# 2. ใช้คำสั่งนี้เพื่อแสดงผลโค้ด HTML ในหน้าเว็บ Streamlit
st.title("MP3 Player Project 🎧")
st.write("ไอเดียจากสนามหญ้า สู่แอปใช้งานจริง")

components.html(html_code, height=600)
