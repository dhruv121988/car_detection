from ultralytics import YOLO
import cv2
import os

def test_model():
    # Load the best trained model
    model = YOLO("runs/detect/train3/weights/best.pt")
    
    # Test on validation images
    val_images_path = "archive/val/images"
    results_dir = "test_results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Get first 5 validation images
    image_files = [f for f in os.listdir(val_images_path) if f.endswith(('.jpg', '.png', '.jpeg'))][:5]
    
    print(f"Testing model on {len(image_files)} images...")
    
    for img_file in image_files:
        img_path = os.path.join(val_images_path, img_file)
        
        # Run inference
        results = model(img_path)
        
        # Save results
        for i, result in enumerate(results):
            # Save annotated image
            output_path = os.path.join(results_dir, f"result_{img_file}")
            result.save(output_path)
            
            # Print detection info
            print(f"\n--- {img_file} ---")
            if result.boxes is not None:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[cls]
                    print(f"Detected: {class_name} (Confidence: {conf:.2f})")
            else:
                print("No detections")

if __name__ == "__main__":
    test_model()
