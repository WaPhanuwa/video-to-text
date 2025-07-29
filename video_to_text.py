#!/usr/bin/env python3
"""
Video to Text Converter
แปลงเสียงจากไฟล์วิดีโอเป็นข้อความโดยใช้ speech recognition
"""

import os
import sys
import speech_recognition as sr
import tempfile
from pathlib import Path

# แก้ปัญหา encoding บน Windows
import locale
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def extract_audio_from_video(video_path, output_audio_path):
    """แยกเสียงจากไฟล์วิดีโอ"""
    # Import moviepy only when needed
    from moviepy.editor import VideoFileClip
    
    video = None
    audio = None
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        # แปลงเป็น WAV ด้วยคุณภาพที่ดีขึ้น
        audio.write_audiofile(
            output_audio_path, 
            logger=None,
            codec='pcm_s16le',  # WAV codec
            ffmpeg_params=['-ac', '1', '-ar', '22050']  # mono, 22kHz (ดีกว่า 16kHz)
        )
        return True
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return False
    finally:
        # ปิดไฟล์อย่างถูกต้อง
        if audio:
            audio.close()
        if video:
            video.close()

def audio_to_text(audio_path, language='th-TH'):
    """แปลงไฟล์เสียงเป็นข้อความ"""
    recognizer = sr.Recognizer()
    
    # ปรับตั้งค่าให้เหมาะสมกับเสียงพูด
    recognizer.energy_threshold = 200  # ลดลงเพื่อจับเสียงเบาได้ดีขึ้น
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8  # รอหยุดพัก 0.8 วินาที
    recognizer.phrase_threshold = 0.3  # ระยะเวลาขั้นต่ำของวลี
    recognizer.non_speaking_duration = 0.5  # ระยะเวลาที่ไม่พูด
    
    try:
        with sr.AudioFile(audio_path) as source:
            print("กำลังอ่านไฟล์เสียง...")
            # ปรับปรุงการอ่านเสียงให้แม่นยำขึ้น
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            
            # อ่านเสียงทั้งหมด
            audio_data = recognizer.record(source)
            
            print("กำลังแปลงเสียงเป็นข้อความ...")
            
            # ลองใช้ Google Speech Recognition พร้อมตัวเลือกที่ดีขึ้น
            try:
                text = recognizer.recognize_google(
                    audio_data, 
                    language=language,
                    show_all=False
                )
                
                if text.strip():
                    print(f"ผลลัพธ์ ({language}): {text}")
                    return text
                else:
                    # ถ้าไม่มีข้อความ ลองภาษาอังกฤษ
                    print("ลองด้วยภาษาอังกฤษ...")
                    text = recognizer.recognize_google(audio_data, language='en-US')
                    return text if text.strip() else "ไม่พบเสียงพูดในไฟล์"
                    
            except sr.RequestError as e:
                return f"ไม่สามารถเชื่อมต่อกับ Google Speech API: {e}"
            except sr.UnknownValueError:
                return "ไม่สามารถแปลงเสียงเป็นข้อความได้ (อาจจะเสียงไม่ชัดหรือไม่มีเสียงพูด)"
            
    except sr.UnknownValueError:
        return "ไม่สามารถแปลงเสียงเป็นข้อความได้ (ไม่พบเสียงพูดที่ชัดเจน)"
    except sr.RequestError as e:
        return f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}"
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {e}"

def video_to_text_converter(video_path, output_text_path=None, language='th-TH'):
    """แปลงวิดีโอเป็นข้อความ"""
    if not os.path.exists(video_path):
        return f"ไม่พบไฟล์: {video_path}"
    
    # สร้างไฟล์เสียงชั่วคราว
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
        temp_audio_path = temp_audio.name
    
    try:
        print(f"กำลังแยกเสียงจาก: {video_path}")
        if not extract_audio_from_video(video_path, temp_audio_path):
            return "ไม่สามารถแยกเสียงจากวิดีโอได้"
        
        print("กำลังแปลงเสียงเป็นข้อความ...")
        text = audio_to_text(temp_audio_path, language)
        
        if output_text_path:
            with open(output_text_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"บันทึกข้อความแล้วที่: {output_text_path}")
        
        return text
        
    except Exception as e:
        return f"เกิดข้อผิดพลาดในการแปลงไฟล์: {str(e)}"
    finally:
        # ลบไฟล์เสียงชั่วคราว
        try:
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
        except:
            pass

def main():
    if len(sys.argv) < 2:
        print("การใช้งาน: python video_to_text.py <path_to_video> [output_text_file] [language]")
        print("ตัวอย่าง: python video_to_text.py video.mp4")
        print("ตัวอย่าง: python video_to_text.py video.mp4 output.txt th-TH")
        print("ภาษาที่รองรับ: th-TH (ไทย), en-US (อังกฤษ), ja-JP (ญี่ปุ่น)")
        return
    
    video_path = sys.argv[1]
    output_text_path = sys.argv[2] if len(sys.argv) > 2 else None
    language = sys.argv[3] if len(sys.argv) > 3 else 'th-TH'
    
    print("=== Video to Text Converter ===")
    print(f"ไฟล์วิดีโอ: {video_path}")
    print(f"ภาษา: {language}")
    
    result = video_to_text_converter(video_path, output_text_path, language)
    
    if result and isinstance(result, str):
        print("\n=== ผลลัพธ์ ===")
        print(result)
        print("\n=== เสร็จสิ้น ===")
    else:
        print("ไม่สามารถแปลงไฟล์ได้")

if __name__ == "__main__":
    main()