st.markdown("""
    <style>
    /* 1. พื้นหลังหลัก: ไล่เฉดสีน้ำเงินเข้มไปหาดำ ให้โลโก้เด่น */
    .stApp {
        background: linear-gradient(145deg, #000033 0%, #000000 100%);
    }
    
    /* 2. ตัวหนังสือทั้งหมดในแอป: สีขาวคมชัด */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px #000000;
    }
    
    /* 3. กล่องข้อความ: ขอบสีเขียวมินต์ ตัวหนังสือสีขาว */
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: #FFFFFF !important;
        border: 2px solid #00CC99 !important;
    }
    
    /* 4. ปุ่มกด: สีแดงนีออน (Red Neon) ตัวหนังสือขาว */
    .stButton>button {
        background: #FF0000 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px;
        font-weight: bold;
        font-size: 20px;
        box-shadow: 0px 0px 15px rgba(255, 0, 0, 0.6);
        transition: 0.3s;
    }
    
    /* 5. เอฟเฟกต์ปุ่มเมื่อกด: เปลี่ยนเป็นสีเขียว */
    .stButton>button:active {
        background: #00FF00 !important;
    }
    
    /* 6. แถบสถานะ (Metric): กรอบสีน้ำเงินสว่าง */
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
    div[data-testid="metric-container"] {
        background-color: rgba(0, 0, 50, 0.5);
        border: 1px solid #0066FF;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
