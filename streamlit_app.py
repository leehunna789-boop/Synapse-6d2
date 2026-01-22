import streamlit as st
import librosa
import numpy as np
import pandas as pd
from PIL import Image

# 1. ส่วนแสดงโลโก้ (ดึงไฟล์ logo.jpg มาโชว์)
try:
    img = Image.open("logo.jpg")
    st.image(img, use_container_width=True)
except:
    st.warning("อย่าลืมเอาไฟล์ logo.jpg ไปวางไว้ในโฟลเดอร์เดียวกันนะลูกพี่!")

# 2. ส่วนหัวข้อและสโลแกน
st.title("🔊 SYNAPSE: Dynamics Meter")
st.write("สโลแกน: 'อยู่นิ่งๆ ไม่เจ็บตัว'") # [cite: 2025-12-20]

# 3. ส่วนการทำงาน
file = st.file_uploader("อัปโหลดไฟล์เสียงเพื่อวัดค่า", type=["wav", "mp3"])

if file:
    y, sr = librosa.load(file)
    rms = librosa.feature.rms(y=y)[0]
    
    st.metric("ความดังเฉลี่ย (Dynamics)", f"{np.mean(rms)*100:.4f}")
    
    st.subheader("📊 กราฟมิติความดัง")
    st.line_chart(pd.DataFrame(rms, columns=["Level"]))
    st.success("วัดค่าสำเร็จ! ส่งผลให้เพื่อนดูได้เลย")
