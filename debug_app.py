from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import os
import traceback

app = Flask(__name__)

# Test model loading separately
def test_model_loading():
    try:
        print("=== TESTING MODEL LOADING IN APP CONTEXT ===")
        model_path = "runs/detect/train3/weights/best.pt"
        print(f"Loading model from: {model_path}")
        
        model = YOLO(model_path)
        print("Model loaded successfully in app context!")
        print(f"Model names: {model.names}")
        
        return model
    except Exception as e:
        print(f"Model loading error: {str(e)}")
        traceback.print_exc()
        return None

# Test model at startup
model = test_model_loading()

@app.route('/')
def index():
    return "Car Damage Detection Debug Server"

@app.route('/test')
def test():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Test inference
        test_image = "archive/val/images/000013.jpg"
        results = model(test_image)
        
        detections = []
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[cls]
                    
                    detections.append({
                        'class': class_name,
                        'confidence': round(conf * 100, 2)
                    })
        
        return jsonify({
            'success': True,
            'detections': detections,
            'total_detections': len(detections)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting debug server...")
    app.run(debug=True, host='127.0.0.1', port=5001)
