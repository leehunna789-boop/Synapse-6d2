from pydub import AudioSegment

def combine_audio(vocal_path, instrumental_path, output_name):
    # 1. โหลดไฟล์เสียง
    print("กำลังโหลดไฟล์...")
    vocal = AudioSegment.from_file(vocal_path)
    instrumental = AudioSegment.from_file(instrumental_path)

    # 2. ปรับความดัง (ถ้าเสียงร้องเบาไป เพิ่มเลขได้ เช่น +3)
    # vocal = vocal + 2 

    # 3. รวมเสียง (Overlay)
    print("กำลังผสมเสียงเข้าด้วยกัน...")
    combined = instrumental.overlay(vocal)

    # 4. ส่งออกไฟล์ผลลัพธ์
    combined.export(output_name, format="wav")
    print(f"เสร็จเรียบร้อย! ไฟล์ของคุณคือ: {output_name}")

# --- ตั้งค่าตรงนี้ ---
vocal_file = "เสียงร้อง-11.wav"        # ไฟล์ที่ได้จาก RVC
instrument_file = "ดนตรี-11.wav"    # ไฟล์ดนตรีเปล่าๆ
output_file = "เพลงเต็ม_เสร็จสมบูรณ์.wav"

combine_audio(vocal_file, instrument_file, output_file)
