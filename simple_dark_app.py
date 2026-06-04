import sys
import os

print(f"Python: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import flask
    print("✅ Flask available!")
    
    import ultralytics
    print("✅ Ultralytics available")
    
    from flask import Flask, render_template_string, request, jsonify, send_from_directory
    from ultralytics import YOLO
    import uuid
    from werkzeug.utils import secure_filename
    
    import torch
    _original_load = torch.load
    torch.load = lambda *args, **kwargs: _original_load(*args, **{**kwargs, 'weights_only': False})
    
    print("✅ All imports successful!")
    
    # Create Flask app
    app = Flask(__name__)
    
    # Create directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    # Load your REAL trained model
    print("Loading YOLO model...")
    model = YOLO("runs/detect/train3/weights/best.pt")
    print("✅ Model loaded successfully!")
    
    class_names = ['dent', 'scratch', 'crack', 'glass shatter', 'lamp broken', 'tire flat']
    
    @app.route('/')
    def index():
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Car Damage Detection - Real AI Model</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container {
                    max-width: 900px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                }
                h1 { color: #2c3e50; text-align: center; margin-bottom: 10px; font-size: 2.5em; }
                .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 40px; font-size: 1.1em; }
                .upload-area {
                    border: 3px dashed #bdc3c7;
                    border-radius: 15px;
                    padding: 60px;
                    text-align: center;
                    background: #f8f9fa;
                    margin-bottom: 30px;
                    transition: all 0.3s ease;
                }
                .upload-area:hover { border-color: #667eea; background: #f0f4ff; }
                .upload-area h3 { color: #2c3e50; margin-bottom: 15px; font-size: 1.5em; }
                .upload-area p { color: #7f8c8d; margin-bottom: 20px; }
                .btn {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    border: none;
                    padding: 12px 30px;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 1em;
                    font-weight: 600;
                    transition: all 0.3s;
                    display: inline-block;
                }
                .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.5); }
                input[type="file"] { display: none; }
                .loading { display: none; text-align: center; padding: 30px; }
                .spinner {
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #667eea;
                    border-radius: 50%;
                    width: 50px; height: 50px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 20px;
                }
                @keyframes spin { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
                .results { display: none; margin-top: 30px; }
                .results-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
                .image-card { text-align: center; }
                .image-card h4 { color: #2c3e50; margin-bottom: 10px; }
                .image-card img { max-width: 100%; border-radius: 10px; box-shadow: 0 5px 20px rgba(0,0,0,0.15); }
                .detections { background: #f8f9fa; border-radius: 10px; padding: 20px; }
                .detections h4 { color: #2c3e50; margin-bottom: 15px; font-size: 1.2em; }
                .detection-item {
                    display: flex; justify-content: space-between; align-items: center;
                    background: white; padding: 12px 15px; border-radius: 8px;
                    margin-bottom: 10px; border-left: 4px solid #667eea;
                }
                .detection-class { font-weight: 600; color: #2c3e50; text-transform: capitalize; }
                .detection-conf {
                    background: #27ae60; color: white;
                    padding: 4px 12px; border-radius: 15px; font-size: 0.9em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚗 Car Damage Detection - Real AI Model</h1>
                <p class="subtitle">Using your trained YOLO model for accurate damage detection</p>

                <div class="upload-area">
                    <h3>📁 Upload Car Image</h3>
                    <p>Upload an image to detect car damage using your trained AI model</p>
                    <label for="fileInput" class="btn">Choose Image</label>
                    <input type="file" id="fileInput" accept="image/*">
                </div>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing image for car damage...</p>
                </div>

                <div class="results" id="results">
                    <div class="results-grid">
                        <div class="image-card">
                            <h4>Original Image</h4>
                            <img id="originalImage" src="" alt="Original">
                        </div>
                        <div class="image-card">
                            <h4>Detected Damage</h4>
                            <img id="resultImage" src="" alt="Results">
                        </div>
                    </div>
                    <div class="detections">
                        <h4>Damage Detected (<span id="detectionCount">0</span> items)</h4>
                        <div id="detectionsList"></div>
                    </div>
                </div>
            </div>

            <script>
                document.getElementById('fileInput').addEventListener('change', function(e) {
                    const file = e.target.files[0];
                    if (file) uploadImage(file);
                });

                function uploadImage(file) {
                    document.getElementById('loading').style.display = 'block';
                    document.getElementById('results').style.display = 'none';
                    const formData = new FormData();
                    formData.append('file', file);
                    fetch('/upload', { method: 'POST', body: formData })
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('loading').style.display = 'none';
                        if (data.success) displayResults(data);
                        else alert('Error: ' + data.error);
                    })
                    .catch(err => {
                        document.getElementById('loading').style.display = 'none';
                        alert('Network error: ' + err.message);
                    });
                }

                function displayResults(data) {
                    document.getElementById('originalImage').src = '/uploads/' + data.original_filename;
                    document.getElementById('resultImage').src = '/results/' + data.result_filename;
                    document.getElementById('detectionCount').textContent = data.total_detections;
                    const list = document.getElementById('detectionsList');
                    list.innerHTML = '';
                    if (data.detections.length === 0) {
                        list.innerHTML = '<p style="color:#7f8c8d">No damage detected</p>';
                    } else {
                        data.detections.forEach(d => {
                            list.innerHTML += `<div class="detection-item">
                                <span class="detection-class">${d.class}</span>
                                <span class="detection-conf">${d.confidence}%</span>
                            </div>`;
                        });
                    }
                    document.getElementById('results').style.display = 'block';
                }
            </script>
        </body>
        </html>
        '''

    @app.route('/upload', methods=['POST'])
    def upload_file():
        try:
            file = request.files['file']
            if file and file.filename != '':
                filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
                filepath = os.path.join('uploads', filename)
                file.save(filepath)

                results = model(filepath)

                detections = []
                for result in results:
                    if result.boxes is not None:
                        for box in result.boxes:
                            cls = int(box.cls[0])
                            conf = float(box.conf[0])
                            class_name = class_names[cls]
                            detections.append({'class': class_name, 'confidence': round(conf * 100, 2)})

                    result_filename = 'result_' + filename
                    result_image_path = os.path.join('results', result_filename)
                    result.save(result_image_path)

                return jsonify({
                    'success': True,
                    'detections': detections,
                    'result_filename': result_filename,
                    'original_filename': filename,
                    'total_detections': len(detections)
                })
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/uploads/<filename>')
    def serve_uploaded_file(filename):
        return send_from_directory('uploads', filename)

    @app.route('/results/<filename>')
    def serve_result_file(filename):
        return send_from_directory('results', filename)

    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=False, host='0.0.0.0', port=5000)

except ImportError as e:
    print(f"Import error: {e}")
    print("Try installing missing packages...")
except Exception as e:
    print(f"Error: {e}")
