import os
import time
import json
import base64
import struct
import requests  # ต้องติดตั้ง: pip install requests

# --- ส่วนที่ 1: ฟังก์ชันระบบ (ห้ามแก้ส่วนนี้) ---

def pcm_to_wav(pcm_data, sample_rate=24000):
    data_size = len(pcm_data)
    header = struct.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 36 + data_size, b'WAVE', b'fmt ', 16, 1, 1, sample_rate, sample_rate * 2, 2, 16, b'data', data_size)
    return header + pcm_data

def generate_lyrics(topic, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": f"แต่งเนื้อเพลงสั้นๆ 4 บรรทัด เรื่อง: {topic} (ภาษาไทย)"}]}]}, headers={'Content-Type': 'application/json'})
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return None

def generate_audio(text, filename, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Aoede"}}}}
    }
    try:
        res = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        audio_data = res.json()['candidates'][0]['content']['parts'][0]['inlineData']['data']
        with open(filename, "wb") as f:
            f.write(pcm_to_wav(base64.b64decode(audio_data)))
        return True
    except:
        return False

# --- ส่วนที่ 2: เริ่มทำงาน (Main) ---
if __name__ == "__main__":
    
    print("--- เริ่มต้นโปรแกรม AI Songwriter ---")

    # ✅ ผมใส่บรรทัดนี้ให้แล้วครับ มันจะดึงรหัสจากเครื่องคุณเอง
    MY_API_KEY = os.environ.get("GEMINI_API_KEY")

    if not MY_API_KEY:
        print("❌ ผิดพลาด: หา GEMINI_API_KEY ในเครื่องไม่เจอครับ")
        exit()
    else:
        print("✅ ดึงกุญแจสำเร็จ! พร้อมทำงาน")

    # เปลี่ยนหัวข้อเพลงตรงนี้ได้ครับ
    topic = "อยู่นิ่งๆ ไม่เจ็บตัว"
    print(f"\n🎵 กำลังแต่งเพลงเรื่อง: {topic}")

    # สั่งทำงาน
    lyrics = generate_lyrics(topic, MY_API_KEY)
    
    if lyrics:
        print(f"\n--- เนื้อเพลง ---\n{lyrics}\n-----------------")
        
        print("🔊 กำลังสร้างไฟล์เสียง...")
        if generate_audio(lyrics, "my_song.wav", MY_API_KEY):
            print("✅ เรียบร้อย! ไฟล์เสียงชื่อ 'my_song.wav' มาแล้วครับ")
        else:
            print("❌ สร้างเสียงไม่สำเร็จ")
    else:
        print("❌ แต่งเพลงไม่สำเร็จ")
