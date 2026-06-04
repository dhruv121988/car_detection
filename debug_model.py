from ultralytics import YOLO
import cv2
import os
import traceback

def debug_model():
    try:
        print("=== DEBUGGING MODEL LOADING ===")
        
        # Check if model file exists
        model_path = "runs/detect/train3/weights/best.pt"
        print(f"Model path: {model_path}")
        print(f"Model file exists: {os.path.exists(model_path)}")
        
        if os.path.exists(model_path):
            file_size = os.path.getsize(model_path)
            print(f"Model file size: {file_size:,} bytes")
        
        # Try to load model
        print("\n=== LOADING MODEL ===")
        model = YOLO(model_path)
        print("Model loaded successfully!")
        
        # Check model info
        print(f"Model names: {model.names}")
        print(f"Model device: {model.device}")
        
        # Test on a simple image
        print("\n=== TESTING INFERENCE ===")
        test_image = "archive/val/images/000013.jpg"
        print(f"Test image: {test_image}")
        print(f"Test image exists: {os.path.exists(test_image)}")
        
        if os.path.exists(test_image):
            results = model(test_image)
            print("Inference completed!")
            
            for result in results:
                print(f"Result shape: {result.boxes.shape if result.boxes is not None else 'No boxes'}")
                if result.boxes is not None and len(result.boxes) > 0:
                    print(f"Number of detections: {len(result.boxes)}")
                    for i, box in enumerate(result.boxes):
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = model.names[cls]
                        print(f"  Detection {i+1}: {class_name} (Confidence: {conf:.2f})")
                else:
                    print("No detections found")
        else:
            print("Test image not found!")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("\nFULL TRACEBACK:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_model()
