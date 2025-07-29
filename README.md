# Video to Text Converter
โปรแกรมแปลงเสียงจากไฟล์วิดีโอเป็นข้อความ

## ความต้องการของระบบ

- Python 3.7 หรือสูงกว่า
- การเชื่อมต่ออินเทอร์เน็ต (สำหรับ Google Speech Recognition)
- Git (สำหรับ clone repository)

## 🔄 สำหรับคนที่โหลดไปแล้ว (อัพเดท)

หากคุณโหลดโปรเจคไปก่อน **29 มกราคม 2025** และเจอปัญหาการติดตั้ง:

```bash
# ดึงการอัพเดทล่าสุด
git pull origin main

# ถอนการติดตั้งเก่า (ถ้ามี)
pip uninstall PyAudio pocketsphinx -y

# ติดตั้งใหม่
pip install -r requirements.txt
```

## การติดตั้งใหม่

### ขั้นตอนที่ 1: ดาวน์โหลดโปรเจค
```bash
git clone https://github.com/WaPhanuwa/video-to-text.git
cd video-to-text
```

### ขั้นตอนที่ 2: สร้าง Virtual Environment (แนะนำ)
```bash
# สร้าง virtual environment
python -m venv venv

# เปิดใช้งาน virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### ขั้นตอนที่ 3: ติดตั้ง Dependencies ตาม OS

#### 🪟 สำหรับ Windows
```bash
# ติดตั้ง packages ทั้งหมด
pip install -r requirements.txt
```

#### 🍎 สำหรับ macOS
```bash
# ติดตั้ง dependencies ที่จำเป็น (สำหรับ moviepy)
brew install ffmpeg

# ติดตั้ง packages
pip install -r requirements.txt
```

#### 🐧 สำหรับ Ubuntu/Debian
```bash
# อัพเดท package list
sudo apt update

# ติดตั้ง dependencies ที่จำเป็น (สำหรับ moviepy)
sudo apt install python3-dev python3-pip ffmpeg

# ติดตั้ง packages
pip install -r requirements.txt
```

### ขั้นตอนที่ 4: สร้างโฟลเดอร์ที่จำเป็น
```bash
mkdir uploads results
```

### ขั้นตอนที่ 5: ทดสอบการติดตั้ง
```bash
# ทดสอบ command line version
python video_to_text.py --help

# หรือทดสอบ web interface
python app.py
```

## วิธีการใช้งาน

### 🌐 Web Interface (แนะนำสำหรับผู้เริ่มต้น)
1. เปิด terminal/command prompt
2. รันคำสั่ง:
```bash
python app.py
```
3. เปิดเบราว์เซอร์ไปที่ `http://localhost:5000`
4. อัพโหลดไฟล์วิดีโอและรอผลลัพธ์

### ⌨️ Command Line Interface

#### การใช้งานพื้นฐาน:
```bash
# แสดงผลบนหน้าจอ
python video_to_text.py your_video.mp4

# บันทึกเป็นไฟล์ข้อความ
python video_to_text.py your_video.mp4 output.txt

# กำหนดภาษา
python video_to_text.py your_video.mp4 output.txt th-TH
```

#### ตัวอย่างการใช้งาน:
```bash
# แปลงวิดีโอภาษาไทย
python video_to_text.py presentation.mp4 transcript.txt th-TH

# แปลงวิดีโอภาษาอังกฤษ
python video_to_text.py lecture.mp4 notes.txt en-US
```

## ภาษาที่รองรับ
- `th-TH` - ภาษาไทย (ค่าเริ่มต้น)
- `en-US` - ภาษาอังกฤษ
- `ja-JP` - ภาษาญี่ปุ่น

## ไฟล์วิดีโอที่รองรับ
- MP4, AVI, MOV, MKV และรูปแบบอื่นๆ ที่ moviepy รองรับ

## 🔧 การแก้ไขปัญหาที่พบบ่อย

### ❌ PyAudio ติดตั้งไม่ได้

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
export LDFLAGS="-L/opt/homebrew/lib"
export CPPFLAGS="-I/opt/homebrew/include"
pip install pyaudio
```

**Ubuntu/Debian:**
```bash
sudo apt install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### ❌ MoviePy หรือ FFmpeg ใช้งานไม่ได้

**Windows:**
1. ดาวน์โหลด FFmpeg จาก https://ffmpeg.org/download.html
2. แตกไฟล์และเพิ่ม path ใน System Environment Variables

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

### ❌ Virtual Environment ใช้งานไม่ได้

```bash
# ลองใช้ python3 แทน python
python3 -m venv venv

# หรือติดตั้ง virtualenv
pip install virtualenv
virtualenv venv
```

### ❌ Permission Error บน macOS

1. ไป System Preferences → Security & Privacy → Privacy → Microphone
2. อนุญาตให้ Terminal เข้าถึงไมโครโฟน

### ❌ Internet Connection Error

- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- Google Speech Recognition ต้องการอินเทอร์เน็ต
- ลองรันทดสอบ: `python -c "import speech_recognition as sr; print('OK')"`

### ❌ Web App แสดง HTTP 500 Error

**ตรวจสอบ server logs:**
```bash
# รัน server และดู error message
python app.py

# ทดสอบ server
curl http://localhost:5000/test
```

**สาเหตุที่พบบ่อย:**
- moviepy import ผิด → แก้ไข: `from moviepy.editor import VideoFileClip`
- ไฟล์วิดีโอเสียหายหรือรูปแบบไม่รองรับ → ใช้ MP4
- หน่วยความจำไม่พอ → ใช้ไฟล์เล็กลง (<50MB)

### ❌ ผลลัพธ์การแปลงไม่แม่นยำ  

**วิธีปรับปรุงความแม่นยำ:**
- ใช้ไฟล์เสียงที่ชัดเจน ไม่มีเสียงรบกวน
- พูดช้าๆ ชัดเจน 
- เลือกภาษาที่ถูกต้อง (th-TH สำหรับไทย)
- ใช้ไฟล์ MP4 ที่มีคุณภาพดี

### ❌ "Failed to fetch" Error

**วิธีแก้ไข:**
```bash
# ตรวจสอบว่า server ทำงาน
python app.py

# เปิดเบราว์เซอร์ใหม่ไปที่
http://localhost:5000

# หรือลองใช้ IP address
http://127.0.0.1:5000
```

## หมายเหตุ
- ต้องการการเชื่อมต่ออินเทอร์เน็ตเพื่อใช้ Google Speech Recognition
- คุณภาพของเสียงจะส่งผลต่อความแม่นยำของการแปลง
- ไฟล์วิดีโอขนาดใหญ่อาจใช้เวลานานในการประมวลผล
- รองรับไฟล์วิดีโอหลายรูปแบบ แต่แนะนำ MP4 สำหรับผลลัพธ์ที่ดีที่สุด