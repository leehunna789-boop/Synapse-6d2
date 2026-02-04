#include <Wire.h>
#include "RTClib.h" // เรียกใช้ Library สำหรับนาฬิกา

RTC_DS3231 rtc; // สร้าง Object ชื่อ rtc สำหรับควบคุมนาฬิกา

const int micPin = A0;    // ต่อขา Out ของ MAX4466 เข้าที่ A0
const int sampleWindow = 50; // เก็บตัวอย่างทุกๆ 50ms (20Hz) เพื่อความแม่นยำ

void setup() {
   Serial.begin(9600); // เปิดหน้าจอ Serial Monitor ที่ Baud Rate 9600
   
   if (!rtc.begin()) {
    Serial.println("Couldn't find RTC module!");
    while (1); // หยุดการทำงานถ้าไม่เจอ RTC
   }
   
   // --- ตั้งเวลาครั้งแรก ---
   // บรรทัดนี้ใช้ตั้งเวลาตามคอมพิวเตอร์ตอนอัพโหลดโค้ด 
   // หลังจากอัพโหลดครั้งแรกแล้ว ให้ใส่ Comment (//) หน้าบรรทัดนี้ทิ้งไว้ 
   // เพื่อให้เวลาเดินต่อไปได้เองโดยไม่รีเซ็ตทุกครั้งที่เปิดเครื่อง
   rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
   // -------------------------
}

void loop() {
   unsigned long startMillis = millis(); 
   unsigned int peakToPeak = 0;   
   unsigned int signalMax = 0;
   unsigned int signalMin = 1024;
   
   // --- เริ่มต้นการสแกนหาค่าเสียงแบบแม่นยำใน 50ms ---
   while (millis() - startMillis < sampleWindow) {
      unsigned int sample = analogRead(micPin);
      if (sample < 1024) {
         if (sample > signalMax) signalMax = sample;  
         if (sample < signalMin) signalMin = sample;  
      }
   }
   // ----------------------------------------------------

   peakToPeak = signalMax - signalMin;  
   double volts = (peakToPeak * 5.0) / 1024; // แปลงเป็นแรงดันไฟฟ้า (โวลต์)

   // --- ดึงข้อมูลเวลาจาก RTC ---
   DateTime now = rtc.now();

   // --- แสดงผลลัพธ์ทาง Serial Monitor ---
   Serial.print("[");
   Serial.print(now.year(), DEC); Serial.print("/");
   Serial.print(now.month(), DEC); Serial.print("/");
   Serial.print(now.day(), DEC); Serial.print(" ");
   Serial.print(now.hour(), DEC); Serial.print(":");
   Serial.print(now.minute(), DEC); Serial.print(":");
   Serial.print(now.second(), DEC);
   Serial.print("] Sound Amplitude: ");
   Serial.print(volts);
   Serial.println(" V");

   delay(100); // หน่วงเวลาเล็กน้อยก่อนวัดรอบถัดไป
}
