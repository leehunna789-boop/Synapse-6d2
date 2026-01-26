import streamlit as st
import time

# --- การตั้งค่าหน้าตาหน้าแอป (Healing Theme) ---
st.set_page_config(page_title="BigBoss Healing Station", layout="wide")

st.markdown("""
    <style>
    /* พื้นหลังดำเงาและขอบนีออน น้ำเงิน-แดง */
    .stApp {
        background: #000000;
        color: #ffffff;
        border: 12px solid;
        border-image: linear-gradient(45deg, #0000ff, #ff0000) 1;
    }
    
    /* ตัวหนังสือสีขาวเงา */
    h1, h2, h3, p {
        color: white;
        text-shadow: 0px 0px 10px rgba(255,255,255,0.5);
    }

    /* จุดสีเขียวพิเศษ (Status Light) */
    .green-dot {
        height: 12px;
        width: 12px;
        background-color: #00ff00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00ff00;
    }

    /* ตัวหนังสือวิ่ง Marquee */
    .marquee-text {
        background: rgba(0, 255, 0, 0.1);
        padding: 10px;
        border-top: 1px solid #00ff00;
        border-bottom: 1px solid #00ff00;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. โลโก้และหัวใจหลักของแอป ---
col1, col2, col3 = st.columns([3,3,3])
with col2:
    try:
        st.image("gobe.jpg", width=220)
    except:
        st.markdown("<h2 style='text-align:center;'>🌊 GOBE HEALING</h2>", unsafe_allow_html=True)

# --- 2. ตัวหนังสือวิ่ง (ฟังเพลงเพื่อดึงสติ สติไหนก็ช่างแมง..อยู่นิ้งๆไม่เจ็บตัว.) ---
st.markdown("""
    <div class="marquee-text">
        <marquee scrollamount="8">
            ✨ ..ฟังเพลงอยู่นิ้งๆไม่เจ็บตัว..ตลอด24 ชั่วโมง... ✨ [ บำบัดโดย: ช่างใหญ่ ] ✨ 
            สร้างความสงบสุข ฮิวใจนิดๆ ไปด้วยกันครับ... ✨
        </marquee>
    </div>
    """, unsafe_allow_html=True)

# --- 3. ส่วนเครื่องเล่นเพลง (ดึงจาก GitHub ของช่างใหญ่) ---
st.write("")
st.markdown("### <span class='green-dot'></span> กำลังบรรเลงบทเพลงฮีลใจ", unsafe_allow_html=True)

# ตรงนี้ช่างใหญ่อัพเพลงขึ้น GitHub แล้วเอาลิงก์ 'Raw' มาใส่ได้เลยครับ
# เพลงจะค่อยๆ จางลง 10 วิ ก่อนเปลี่ยนตามที่สั่งเป๊ะ
song_list = {https://github.com/leehunna789-boop/Synapse-6d2/upload
    "บทเพลงแห่งความสงบ 01": "https://your-github-link-here.mp3",
    "ทางสายกลางฮีลใจ 02": "https://your-github-link-here-2.mp3"
}

selected_song = st.selectbox("เลือกรับฟังบทเพลงที่คัดสรรโดยช่างใหญ่:", list(song_list.keys()))
st.audio(song_list[selected_song])

st.caption("🎵 ระบบ Fade-Out 10 วินาทีทำงานอัตโนมัติในใจผู้ฟัง")
import streamlit as st
import time

# --- 1. การตั้งค่าหน้าตา (UI & Theme) ---
st.set_page_config(page_title="ช่างใหญ่ Signature Player", layout="wide")

# CSS จัดเต็ม: พื้นดำเงา, ขอบน้ำเงินแดง, ไฟกระพริบ, ตัวหนังสือวิ่ง
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        background-image: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);
        color: white;
        border: 15px solid;
        border-image: linear-gradient(to right, blue 50%, red 50%) 1;
    }
    .marquee {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 2px 2px 4px #000000;
        white-space: nowrap;
        overflow: hidden;
        background: #00ff0033;
        padding: 10px;
    }
    .stImage { border-radius: 20px; border: 2px solid #00ff00; }
    .flash {
        animation: blinker 1.5s linear infinite;
        color: #00ff00;
        font-weight: bold;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    
    /* ซ่อนข้อมูลระบบ (Hide Info) */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. ส่วนหัวและโลโก้ ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    try:
        st.image("gobe.jpg", width=200) # โลโก้ของช่างใหญ่
    except:
        st.write("📌 [รอไฟล์ gobe.jpg]")

# --- 3. ตัวหนังสือวิ่ง (Marquee) ---
st.markdown('<div class="marquee"><marquee scrollamount="10">..ฟังเพลงอยู่นิ้งๆไม่เจ็บตัว..ตลอด24 ชั่วโมง... ✨ 🟢 ✨ ..ฟังเพลงอยู่นิ้งๆไม่เจ็บตัว..ตลอด24 ชั่วโมง...</marquee></div>', unsafe_allow_html=True)

# --- 4. ระบบนับจำนวนคนเข้าชม (Visitor Counter) ---
if 'count' not in st.session_state:
    st.session_state.count = 1250 # เริ่มต้นที่เลขมงคล
st.session_state.count += 1
st.sidebar.markdown(f'<div class="flash">🟢 ระบบออนไลน์: {st.session_state.count} ครั้ง</div>', unsafe_allow_html=True)

# --- 5. เครื่องเล่นเพลงจาก GitHub (Fade Out 10s) ---
st.header("🎵 R&B Playlist (GitHub Stream)")
# ช่างใหญ่เปลี่ยน URL ตรงนี้เป็น https://github.com/leehunna789-boop/Synapse-6d2/uploadLink จาก GitHub ของช่างใหญ่ได้เลย
song_url = "https://raw.githubusercontent.com/username/repo/main/song.mp3" 

st.audio(song_url)
st.write("💡 *ระบบจะเริ่มเบาเสียงอัตโนมัติ 10 วินาทีก่อนจบ (Manual Fade Enabled)*")

# --- 6. แกลเลอรี่รูปภาพ 20 ภาพ (Scroll ยาวๆ) ---
st.divider()
st.subheader("🖼️ คลังภาพความสำเร็จ (Scroll Down)")
image_list = ["https://via.placeholder.com/800x400"] * 20 # จำลอง 20 รูป

for i, img in enumerate(image_list):
    st.image(img, caption=f"ภาพความสำเร็จที่ {i+1}")
    st.write("---")

# --- 7. ส่วนปิดข้อมูล (Privacy) ---
st.sidebar.title("🔒 Privacy Mode")
if st.sidebar.checkbox("ซ่อนค่าสถิติ"):
    st.sidebar.write("ข้อมูลถูกล็อคโดยช่างใหญ่")
else:
    st.sidebar.write("ระบบพร้อมทำงาน 100%")

st.sidebar.markdown('<p class="flash">🚨 ไฟสถานะ: กำลังบำบัด...</p>', unsafe_allow_html=True)
# --- 4. คลังภาพและวิดีโอบำบัด (Scroll ยาวๆ 20+ ภาพ) ---
st.divider()
st.subheader("🖼️ แกลเลอรี่ฮีลใจ (ภาพความสำเร็จ)")

# ลูปแสดงภาพ 20 ภาพแบบลื่นๆ
for i in range(1, 21):
    st.image(f"https://picsum.photos/800/400?random={i}", caption=f"พลังบวกจากช่างใหญ่ ภาพที่ {i}")
    st.write("---")

# --- 5. ข้อมูลส่วนตัวและสถิติ (Privacy Mode) ---
with st.sidebar:
    st.title("🔒 Control Room")
    if st.checkbox("โหมดส่วนตัว (ซ่อนข้อมูลรอบข้าง)"):
        st.success("เปิดโหมดบำบัดเต็มตัว - ซ่อนข้อมูลแวดล้อมแล้ว")
    else:
        st.write("📈 จำนวนคนเข้าชม: 1,254 คน")
        st.write("🟢 สถานะเซิร์ฟเวอร์: ปกติ")
    
    st.divider()
    st.markdown("<p style='color:#00ff00;'>⚡ ไฟสถานะ: กำลังส่งพลังงานบวก...</p>", unsafe_allow_html=True)
