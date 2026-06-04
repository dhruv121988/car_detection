from ultralytics import YOLO
import cv2
import os

def test_scratch_detection():
    print("=== TESTING SCRATCH DETECTION ===")
    
    # Load the model
    model = YOLO("runs/detect/train3/weights/best.pt")
    print(f"Model names: {model.names}")
    
    # Test on validation images that should have scratches
    val_images_path = "archive/val/images"
    image_files = [f for f in os.listdir(val_images_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    scratch_found = False
    total_images = 0
    
    for img_file in image_files[:10]:  # Test first 10 images
        img_path = os.path.join(val_images_path, img_file)
        total_images += 1
        
        # Run inference
        results = model(img_path)
        
        # Check for scratches
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[cls]
                    
                    if class_name == 'scratch':
                        scratch_found = True
                        print(f"✅ SCRATCH DETECTED in {img_file}: {class_name} (Confidence: {conf:.2f})")
                    elif conf > 0.3:  # Show other detections with decent confidence
                        print(f"   {img_file}: {class_name} (Confidence: {conf:.2f})")
    
    print(f"\n=== SUMMARY ===")
    print(f"Images tested: {total_images}")
    print(f"Scratches detected: {'YES' if scratch_found else 'NO'}")
    
    if not scratch_found:
        print("\n⚠️  No scratches detected!")
        print("Possible issues:")
        print("1. Model confidence threshold too high")
        print("2. Model undertrained (only 7/50 epochs)")
        print("3. Class mapping issue")
        
        # Test with lower confidence threshold
        print("\n=== TESTING WITH LOWER CONFIDENCE ===")
        for img_file in image_files[:3]:
            img_path = os.path.join(val_images_path, img_file)
            results = model(img_path, conf=0.1)  # Very low confidence
            
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = model.names[cls]
                        
                        print(f"   {img_file}: {class_name} (Low conf: {conf:.2f})")

if __name__ == "__main__":
    test_scratch_detection()
