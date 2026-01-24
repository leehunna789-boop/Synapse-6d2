<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Music Player - Bright Idea!</title>
    <style>
        :root {
            --primary-color: #2ecc71;
            --bg-color: #1a1a1a;
            --card-bg: #2d2d2d;
            --text-color: #ffffff;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }

        .player-card {
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            width: 350px;
            text-align: center;
        }

        .track-info h2 { margin-bottom: 5px; font-size: 1.2rem; }
        .track-info p { color: #aaa; margin-top: 0; }

        .controls {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin: 20px 0;
        }

        button {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            font-size: 1.5rem;
            transition: transform 0.2s;
        }

        button:hover { transform: scale(1.1); color: var(--primary-color); }

        #playPauseBtn { font-size: 3rem; }

        .volume-container, .progress-container {
            margin: 15px 0;
            width: 100%;
        }

        input[type="range"] { width: 100%; accent-color: var(--primary-color); }

        .playlist {
            text-align: left;
            max-height: 150px;
            overflow-y: auto;
            margin-top: 20px;
            border-top: 1px solid #444;
            padding-top: 10px;
        }

        .playlist-item {
            padding: 8px;
            cursor: pointer;
            border-radius: 5px;
            font-size: 0.9rem;
        }

        .playlist-item:hover { background: #3d3d3d; }
        .active-track { color: var(--primary-color); font-weight: bold; }

        .upload-section { margin-top: 15px; }
        .custom-file-upload {
            display: inline-block;
            padding: 8px 20px;
            background: var(--primary-color);
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
        }

        #shareBtn {
            margin-top: 10px;
            font-size: 0.9rem;
            color: #3498db;
            text-decoration: underline;
        }
    </style>
</head>
<body>

<div class="player-card">
    <div class="track-info">
        <h2 id="title">เลือกเพลงเพื่อเริ่มฟัง</h2>
        <p id="artist">กดปุ่มสีเขียวเพื่อเพิ่มเพลง</p>
    </div>

    <div class="progress-container">
        <input type="range" id="progressBar" value="0" step="1">
    </div>

    <div class="controls">
        <button onclick="prevTrack()">⏮</button>
        <button id="playPauseBtn" onclick="togglePlay()">▶️</button>
        <button onclick="nextTrack()">⏭</button>
    </div>

    <div class="volume-container">
        <span>🔊</span>
        <input type="range" id="volumeControl" min="0" max="1" step="0.1" value="1">
    </div>

    <div class="upload-section">
        <label class="custom-file-upload">
            <input type="file" id="fileInput" multiple accept="audio/*" style="display:none;">
            ➕ เพิ่มเพลง MP3
        </label>
    </div>

    <div class="playlist" id="playlist">
        </div>

    <button id="shareBtn" onclick="shareApp()">🔗 แชร์แอปนี้ให้เพื่อน</button>
</div>

<audio id="audioPlayer"></audio>

<script>
    const audio = document.getElementById('audioPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const fileInput = document.getElementById('fileInput');
    const playlistDisplay = document.getElementById('playlist');
    const title = document.getElementById('title');
    const progressBar = document.getElementById('progressBar');
    const volumeControl = document.getElementById('volumeControl');

    let songs = [];
    let currentSongIndex = 0;

    // ระบบเพิ่มเพลง
    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        files.forEach(file => {
            const url = URL.createObjectURL(file);
            songs.push({ name: file.name, url: url });
        });
        updatePlaylist();
        if (songs.length === files.length) loadSong(0);
    });

    function updatePlaylist() {
        playlistDisplay.innerHTML = '';
        songs.forEach((song, index) => {
            const div = document.createElement('div');
            div.className = `playlist-item ${index === currentSongIndex ? 'active-track' : ''}`;
            div.innerText = `${index + 1}. ${song.name}`;
            div.onclick = () => loadSong(index);
            playlistDisplay.appendChild(div);
        });
    }

    function loadSong(index) {
        currentSongIndex = index;
        audio.src = songs[index].url;
        title.innerText = songs[index].name;
        updatePlaylist();
        playSong();
    }

    function togglePlay() {
        if (audio.paused) playSong();
        else pauseSong();
    }

    function playSong() {
        if (!audio.src) return;
        audio.play();
        playPauseBtn.innerText = '⏸';
    }

    function pauseSong() {
        audio.pause();
        playPauseBtn.innerText = '▶️';
    }

    function nextTrack() {
        currentSongIndex = (currentSongIndex + 1) % songs.length;
        loadSong(currentSongIndex);
    }

    function prevTrack() {
        currentSongIndex = (currentSongIndex - 1 + songs.length) % songs.length;
        loadSong(currentSongIndex);
    }

    // ระบบเล่นต่อเนื่อง
    audio.addEventListener('ended', nextTrack);

    // ปรับเสียง
    volumeControl.addEventListener('input', (e) => audio.volume = e.target.value);

    // Progress Bar
    audio.addEventListener('timeupdate', () => {
        progressBar.max = audio.duration;
        progressBar.value = audio.currentTime;
    });

    progressBar.addEventListener('input', () => audio.currentTime = progressBar.value);

    // ปุ่มแชร์
    function shareApp() {
        if (navigator.share) {
            navigator.share({
                title: 'My Music Player',
                text: 'ลองใช้แอปเครื่องเล่นเพลงที่ผมสร้างสิ!',
                url: window.location.href
            });
        } else {
            alert("คัดลอกลิงก์ส่งให้เพื่อนได้เลย: " + window.location.href);
        }
    }
</script>

</body>
</html>
