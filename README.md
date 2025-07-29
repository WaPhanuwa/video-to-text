# Video to Text Converter
โปรแกรมแปลงเสียงจากไฟล์วิดีโอเป็นข้อความ

## ความต้องการของระบบ

- Python 3.7 หรือสูงกว่า
- การเชื่อมต่ออินเทอร์เน็ต (สำหรับ Google Speech Recognition)
- ไมโครโฟนและลำโพง (หากใช้งาน PyAudio)

## การติดตั้ง

### 1. Clone หรือ Download โปรเจค
```bash
git clone <repository-url>
cd video-to-text
```

### 2. สร้าง Virtual Environment (แนะนำ)
```bash
python -m venv venv

# สำหรับ Windows
venv\Scripts\activate

# สำหรับ macOS/Linux
source venv/bin/activate
```

### 3. ติดตั้ง Dependencies

#### สำหรับ Windows:
```bash
# ติดตั้ง PyAudio ก่อน (ถ้าเกิดปัญหา)
pip install pipwin
pipwin install pyaudio

# ติดตั้ง dependencies ทั้งหมด
pip install -r requirements.txt
```

#### สำหรับ macOS:
```bash
# ติดตั้ง dependencies ที่จำเป็นก่อน
brew install portaudio
pip install -r requirements.txt
```

#### สำหรับ Ubuntu/Debian:
```bash
# ติดตั้ง dependencies ที่จำเป็นก่อน
sudo apt-get install python3-dev python3-pip libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
pip install -r requirements.txt
```

### 4. สร้าง Folders ที่จำเป็น
```bash
mkdir uploads results
```

## การใช้งาน

### วิธีที่ 1: Web Interface (แนะนำ)
```bash
python app.py
```
จากนั้นเปิดเบราว์เซอร์ที่ `http://localhost:5000`

### วิธีที่ 2: Command Line

#### แบบพื้นฐาน (แสดงผลบนหน้าจอ):
```bash
python video_to_text.py video.mp4
```

#### บันทึกเป็นไฟล์ข้อความ:
```bash
python video_to_text.py video.mp4 output.txt
```

#### กำหนดภาษา:
```bash
python video_to_text.py video.mp4 output.txt th-TH
```

## ภาษาที่รองรับ
- `th-TH` - ภาษาไทย (ค่าเริ่มต้น)
- `en-US` - ภาษาอังกฤษ
- `ja-JP` - ภาษาญี่ปุ่น

## ไฟล์วิดีโอที่รองรับ
- MP4, AVI, MOV, MKV และรูปแบบอื่นๆ ที่ moviepy รองรับ

## การแก้ไขปัญหาที่พบบ่อย

### PyAudio ติดตั้งไม่ได้
```bash
# สำหรับ Windows
pip install pipwin
pipwin install pyaudio

# สำหรับ macOS
brew install portaudio
export LDFLAGS="-L/opt/homebrew/lib"
export CPPFLAGS="-I/opt/homebrew/include"
pip install pyaudio

# สำหรับ Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
```

### MoviePy ใช้งานไม่ได้
```bash
# ติดตั้ง ffmpeg
# Windows: ดาวน์โหลดจาก https://ffmpeg.org/download.html
# macOS:
brew install ffmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg
```

### ปัญหา Permission บน macOS
```bash
# อนุญาตให้ Terminal เข้าถึงไมโครโฟน
# System Preferences > Security & Privacy > Privacy > Microphone
```

## หมายเหตุ
- ต้องการการเชื่อมต่ออินเทอร์เน็ตเพื่อใช้ Google Speech Recognition
- คุณภาพของเสียงจะส่งผลต่อความแม่นยำของการแปลง
- ไฟล์วิดีโอขนาดใหญ่อาจใช้เวลานานในการประมวลผล
- รองรับไฟล์วิดีโอหลายรูปแบบ แต่แนะนำ MP4 สำหรับผลลัพธ์ที่ดีที่สุด