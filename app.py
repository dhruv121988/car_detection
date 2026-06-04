from flask import Flask, render_template, request, jsonify, send_from_directory
from ultralytics import YOLO
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from cost_estimator import CostEstimator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Load the trained model
model = YOLO("runs/detect/train3/weights/best.pt")

# Initialize cost estimator
cost_estimator = CostEstimator()

# Class names
class_names = ['dent', 'scratch', 'crack', 'glass shatter', 'lamp broken', 'tire flat']

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Run detection with lower confidence threshold
            results = model(filepath, conf=0.25)
            
            # Process results
            detections = []
            result_image = None
            
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = model.names[cls]
                        
                        detections.append({
                            'class': class_name,
                            'confidence': round(conf * 100, 2),
                            'bbox': box.xyxy[0].tolist()
                        })
                
                # Save result image
                result_image_path = os.path.join(app.config['RESULT_FOLDER'], 'result_' + filename)
                result.save(result_image_path)
                result_image = 'results/result_' + filename
            
            # Generate cost estimation report
            cost_report = cost_estimator.generate_full_report(detections)
            
            return jsonify({
                'success': True,
                'detections': detections,
                'result_image': result_image,
                'original_image': 'uploads/' + filename,
                'total_detections': len(detections),
                'cost_report': cost_report
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/camera_capture', methods=['POST'])
def camera_capture():
    try:
        # Get base64 image data
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({'error': 'No image data'}), 400
        
        # Convert base64 to image
        import base64
        image_data = image_data.split(',')[1]  # Remove data:image/jpeg;base64, prefix
        image_bytes = base64.b64decode(image_data)
        
        # Save image
        filename = str(uuid.uuid4()) + '_camera.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        # Run detection with lower confidence threshold
        results = model(filepath, conf=0.25)
        
        # Process results
        detections = []
        result_image = None
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[cls]
                    
                    detections.append({
                        'class': class_name,
                        'confidence': round(conf * 100, 2),
                        'bbox': box.xyxy[0].tolist()
                    })
            
            # Save result image
            result_image_path = os.path.join(app.config['RESULT_FOLDER'], 'result_' + filename)
            result.save(result_image_path)
            result_image = 'results/result_' + filename
        
        # Generate cost estimation report
        cost_report = cost_estimator.generate_full_report(detections)
        
        return jsonify({
            'success': True,
            'detections': detections,
            'result_image': result_image,
            'original_image': 'uploads/' + filename,
            'total_detections': len(detections),
            'cost_report': cost_report
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Car Damage Detection Web App...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
