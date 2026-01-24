import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="Heavy Duty Player", layout="wide")

# 2. ผ้าคลุมล่องหน (ซ่อนปุ่มแดง/ม่วง และเมนูทั้งหมด)
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

# 3. ตัวเครื่องเล่น (ใส่ HTML/CSS/JS ไว้ในนี้ทั้งหมด)
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        :root { --neon: #00ff88; --bg: #0a0a0a; --border-width: 10px; }
        body { background: var(--bg); color: white; font-family: sans-serif; display: flex; justify-content: center; padding: 20px; }
        .player-box {
            border: var(--border-width) solid var(--neon);
            border-radius: 50px; padding: 40px; width: 320px; text-align: center;
            background: #111; box-shadow: 0 0 30px rgba(0,255,136,0.2);
        }
        .btn-main { background: var(--neon); border: none; width: 80px; height: 80px; border-radius: 50%; font-size: 2rem; cursor: pointer; }
        .slider { width: 100%; accent-color: var(--neon); margin: 20px 0; }
    </style>
</head>
<body>
    <div class="player-box">
        <h2 style="color:var(--neon)">เสียง...</h2>
        <div style="background:#222; padding:15px; border-radius:20px; margin-bottom:20px;">
            <small>BASS / MIX</small>
            <input type="range" class="slider">
        </div>
        <button class="btn-main">▶</button>
        <p style="margin-top:20px; color:var(--neon)">[ + ใส่แผ่นเพลง ]</p>
    </div>
</body>
</html>
"""

# 4. แสดงผลแอป
components.html(html_code, height=700)
