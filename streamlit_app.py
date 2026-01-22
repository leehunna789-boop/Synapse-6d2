import librosa
import numpy as np
import scipy.stats

# --- 1. พิมพ์ชื่อไฟล์ที่คุณต้องการวัดค่า (เลือกทีละไฟล์จากในเครื่องคุณ) ---
# เช่น: "การเดินทางของฉัน_ร้อง.2.mp3" หรือ "การเดินทางของฉัน กลอง.mp3"
target_file = "การเดินทางของฉัน_ร้อง.2.mp3" 

def extract_real_dna(filename):
    try:
        # โหลดไฟล์เสียงลงหน่วยความจำเครื่อง
        y, sr = librosa.load(filename, sr=None)
        
        # 8-9. Formants (F1, F2) - วัดรูปปากและการวางลิ้นแบบสมจริง
        pre_emp = librosa.effects.preemphasis(y)
        a = librosa.lpc(pre_emp, order=int(2 + sr / 1000))
        roots = [r for r in np.roots(a) if np.imag(r) > 0]
        f_vals = sorted(np.arctan2(np.imag(roots), np.real(roots)) * (sr / (2 * np.pi)))
        f1, f2 = (f_vals[0], f_vals[1]) if len(f_vals) > 1 else (0, 0)

        # 10. Spectral Tilt - วัดความนุ่มนวล/ความกระด้างของอารมณ์
        S = np.abs(librosa.stft(y))
        freqs = librosa.fft_frequencies(sr=sr)
        slope, _, _, _, _ = scipy.stats.linregress(freqs, np.mean(S, axis=1))

        # 11. HNR (Harmonics-to-Noise) - วัด "ลมหายใจ" (หัวใจของความสมจริง)
        harmonic, percussive = librosa.effects.hpss(y)
        hnr = 10 * np.log10(np.sum(harmonic**2) / np.sum(percussive**2)) if np.sum(percussive**2) > 0 else 0

        # 12. RT60 Proxy - วัดมิติพื้นที่ (ห้องก้องหรือห้องแห้ง)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        rt60 = abs(1 / np.mean(np.diff(onset_env))) if len(onset_env) > 1 else 0

        print(f"\n--- รายงาน DNA เสียง: {filename} ---")
        print(f"8.  F1 (ความกว้างปาก): {f1:.2f} Hz")
        print(f"9.  F2 (ตำแหน่งลิ้น): {f2:.2f} Hz")
        print(f"10. Tilt (ความนุ่ม): {slope:.8f}")
        print(f"11. HNR (ลมหายใจ): {hnr:.2f} dB")
        print(f"12. RT60 (มิติห้อง): {rt60:.4f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# สั่งทำงาน
extract_real_dna(target_file)
