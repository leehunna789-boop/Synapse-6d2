import streamlit as st
import numpy as np
import time
import os

# --- 1. การตั้งค่าหน้าจอและสไตล์พรีเมียม (Neon Glow Design) ---
st.set_page_config(page_title="SYNAPSE 6D ENERGY PRO", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    /* พื้นหลังแบบมืดไล่ระดับสี */
    .stApp { 
        background: radial-gradient(circle, #0c074e 0%, #050531 60%, #020111 100%); 
        color: #ffffff; 
    }
    
    /* ตัวหนังสือเรืองแสง (Glow Effect) */
    .glow-text {
        color: #fff;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        text-shadow: 0 0 10px #00FFFF, 0 0 20px #00FFFF, 0 0 30px #00FFFF; /* เปลี่ยนสีเป็นฟ้า-เขียว เพื่อธีมโลก */
        margin-bottom: 20px;
    }
    
    .slogan-glow {
        color: #00FFD1; /* สีเขียวมิ้นต์ เพื่อธีมโลก */
        text-align: center;
        font-size: 24px;
        font-style: italic;
        text-shadow: 0 0 5px #fff, 0 0 10px #00FFD1;
        margin-bottom: 30px;
    }

    /* ปุ่มกดแบบมีแสงรอบๆ */
    .stButton>button { 
        background: linear-gradient(90deg, #00FFFF, #00FF8C, #00FFD1); /* สีฟ้า-เขียว เพื่อธีมโลก */
        color: white; 
        border-radius: 50px; 
        border: none; 
        width: 100%; 
        height: 4.5em; 
        font-weight: bold; 
        font-size: 22px;
        box-shadow: 0 0 20px rgba(0, 255, 209, 0.6);
        transition: 0.5s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 40px rgba(0, 255, 209, 0.9);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ระบบ Sound Engine เลือกดนตรีตามอารมณ์และวิดีโอ "World Healing" ---
def get_therapy(user_text):
    text = user_text.lower()
    
    # วิดีโอ 4K คุณภาพสูงที่สื่อถึงธรรมชาติและการฟื้นฟูโลก
    world_healing_video = "https://www.youtube.com/watch?v=CxQ2xX6iM98" # คลิป 4K ธรรมชาติ สงบเงียบ
    
    if any(word in text for word in ['เหนื่อย', 'เครียด', 'เศร้า', 'ท้อ']):
        return {
            "title": "💎 Deep Healing Piano & Ocean Waves (World Resonance)",
            "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3", # เสียงธรรมชาติผสมดนตรี
            "video": world_healing_video,
            "desc": "คลื่นเสียงบำบัดเพื่อความสงบและการเชื่อมโยงกับโลก"
        }
    elif any(word in text for word in ['สุข', 'ดี', 'ยิ้ม', 'รัก', 'พลัง']):
        return {
            "title": "✨ Global Harmony Symphony (Renewable Energy)",
            "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", # ดนตรีบำบัดเชิงบวก
            "video": world_healing_video,
            "desc": "เพิ่มความสดชื่นและกระตุ้นพลังงานเพื่อการฟื้นฟูโลก"
        }
    else: # อารมณ์ทั่วไป หรือต้องการการปรับสมดุล
        return {
            "title": "🌿 Earth's Embrace (Forest & River Soundscape)",
            "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", # เสียงน้ำไหลในป่า
            "video": world_healing_video,
            "desc": "เสียงธรรมชาติบริสุทธิ์เพื่อความสมดุลและพลังแห่งการเยียวยา"
        }

# --- 3. ส่วนการแสดงผลโลโก้และหัวข้อ ---
st.markdown('<div class="glow-text">SYNAPSE 6D ENERGY PRO</div>', unsafe_allow_html=True)

logo_path = "logo.jpg"
if os.path.exists(logo_path):
    st.image(logo_path, use_container_width=True) # แสดงโลโก้ของคุณ

st.markdown('<div class="slogan-glow">"พลังงานเพื่อโลก... อยู่นิ่งๆ ไม่เจ็บตัว"</div>', unsafe_allow_html=True) # เพิ่มธีมโลกในสโลแกน

# --- 4. ฟังก์ชันพิเศษ: Zen Energy Charge ---
st.write("---")
st.subheader("🧘‍♂️ ระบบชาร์จพลังงานเพื่อโลก (Zen Earth Charge)")
if st.toggle("ACTIVATE WORLD HEALING MODE"):
    st.info("กรุณานิ่ง... ระบบกำลังซิงค์พลังงานบริสุทธิ์จากโลก")
    bar = st.progress(0)
    for p in range(101):
        time.sleep(0.04)
        bar.progress(p)
    st.success("✨ ชาร์จพลังงานโลกสำเร็จ! คุณได้เชื่อมโยงกับกระแสแห่งการเยียวยา")

# --- 5. ระบบบำบัด Fully Automated (World Healing Edition) ---
st.write("---")
user_feeling = st.text_area("วันนี้สภาวะจิตใจและพลังงานของคุณเป็นอย่างไร?", placeholder="ระบุสิ่งที่ต้องการบำบัด หรือความมุ่งมั่นที่จะช่วยโลก...")

if st.button("🌍 ACTIVATE GLOBAL ENERGY THERAPY"):
    if user_feeling:
        therapy = get_therapy(user_feeling)
        with st.status("⚡ กำลังเชื่อมต่อ SYNAPSE 6D กับพลังงานฟื้นฟูโลก...", expanded=True):
            time.sleep(1.5)
            st.write(f"🎵 กำลังจูนดนตรีเพื่อโลก: {therapy['title']}")
            time.sleep(1.2)
        
        st.balloons()
        
        # แสดงผลเสียงดนตรีสมจริง
        st.subheader(f"🔊 Playing: {therapy['title']}")
        st.audio(therapy['audio'])
        st.caption(therapy['desc'])
        
        st.write("---")
        # แสดงผลวิดีโอบำบัด 4K เพื่อโลก
        st.subheader("📺 Visual Energy for World Healing (4K)")
        st.video(therapy['video']) # วิดีโอ 4K ธรรมชาติที่สื่อถึงการฟื้นฟูโลก
        
        st.success(f"พลังงานเพื่อการเยียวยาโลกสำหรับ '{user_feeling}' ได้รับการกระตุ้นแล้ว... 'อยู่นิ่งๆ ไม่เจ็บตัว' และส่งพลังงานบวกไปให้โลกนะครับ")
    else:
        st.warning("กรุณาระบุความรู้สึกหรือความมุ่งมั่นของคุณ")

# --- 6. ส่วนท้าย (Footer) ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #444;'>💎 SYNAPSE 6D HIGH-PERFORMANCE SYSTEM<br>POWERED BY EARTH'S ENERGY</p>", unsafe_allow_html=True)
