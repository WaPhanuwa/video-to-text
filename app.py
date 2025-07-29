#!/usr/bin/env python3
"""
Video to Text Web Application
เว็บแอปสำหรับแปลงเสียงจากไฟล์วิดีโอเป็นข้อความ
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
from werkzeug.utils import secure_filename
from video_to_text import video_to_text_converter
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# สร้างโฟลเดอร์หากไม่มี
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'}
LANGUAGES = {
    'th-TH': 'ไทย',
    'en-US': 'English',
    'ja-JP': '日本語',
    'ko-KR': '한국어',
    'zh-CN': '中文'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/test', methods=['GET', 'POST'])
def test_endpoint():
    """Test endpoint to check if server is working"""
    response = jsonify({
        'status': 'OK',
        'message': 'Server is working',
        'method': request.method
    })
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    print("=== Upload request received ===")
    
    # Add CORS headers manually
    response_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Test imports first
    try:
        from video_to_text import video_to_text_converter
        print("video_to_text import successful")
    except Exception as e:
        print(f"Error importing video_to_text: {e}")
        response = jsonify({'error': f'Server configuration error: {e}'})
        for key, value in response_headers.items():
            response.headers[key] = value
        return response, 500
    
    try:
        if 'video' not in request.files:
            response = jsonify({'error': 'ไม่พบไฟล์วิดีโอ'})
            for key, value in response_headers.items():
                response.headers[key] = value
            return response, 400
        
        file = request.files['video']
        language = request.form.get('language', 'th-TH')
        
        if file.filename == '':
            return jsonify({'error': 'ไม่ได้เลือกไฟล์'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'รองรับเฉพาะไฟล์วิดีโอ: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400
        
        # สร้างชื่อไฟล์ที่ไม่ซ้ำ
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # บันทึกไฟล์
        try:
            print(f"Saving file to: {video_path}")
            file.save(video_path)
            print(f"File saved successfully, size: {os.path.getsize(video_path)} bytes")
        except Exception as e:
            print(f"Error saving file: {e}")
            raise
        
        # แปลงเป็นข้อความ
        try:
            print(f"Starting conversion for file: {video_path}, language: {language}")
            result_text = video_to_text_converter(video_path, language=language)
            print(f"Conversion result: {result_text[:100]}..." if result_text and len(result_text) > 100 else f"Conversion result: {result_text}")
        except Exception as e:
            print(f"Error in video_to_text_converter: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # ลบไฟล์วิดีโอหลังจากแปลงเสร็จ
        try:
            import time
            time.sleep(1)  # รอให้ไฟล์ปิดสมบูรณ์
            if os.path.exists(video_path):
                os.remove(video_path)
        except Exception as e:
            print(f"Warning: Could not delete video file: {e}")
        
        print(f"Debug - result_text: {result_text}")  # Debug line
        
        if result_text and not result_text.startswith('ไม่สามารถ') and not result_text.startswith('เกิดข้อผิดพลาด'):
            # บันทึกผลลัพธ์
            result_filename = f"result_{uuid.uuid4()}.txt"
            result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
            
            with open(result_path, 'w', encoding='utf-8') as f:
                f.write(f"ไฟล์: {filename}\n")
                f.write(f"ภาษา: {LANGUAGES.get(language, language)}\n")
                f.write(f"วันที่: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n\n")
                f.write(result_text)
            
            response = jsonify({
                'success': True,
                'text': result_text,
                'download_url': f'/download/{result_filename}'
            })
            for key, value in response_headers.items():
                response.headers[key] = value
            return response
        else:
            response = jsonify({'error': result_text or 'ไม่สามารถแปลงไฟล์ได้'})
            for key, value in response_headers.items():
                response.headers[key] = value
            return response, 500
            
    except Exception as e:
        print(f"=== ERROR: {str(e)} ===")
        import traceback
        traceback.print_exc()
        response = jsonify({'error': f'เกิดข้อผิดพลาด: {str(e)}'})
        for key, value in response_headers.items():
            response.headers[key] = value
        return response, 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['RESULTS_FOLDER'], filename),
            as_attachment=True,
            download_name=f"transcription_{filename}"
        )
    except FileNotFoundError:
        return "ไฟล์ไม่พบ", 404

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)