from ultralytics import YOLO
import os

def find_multiple_damages():
    print("=== FINDING IMAGES WITH MULTIPLE DAMAGE TYPES ===")
    
    # Load the model
    model = YOLO("runs/detect/train3/weights/best.pt")
    
    # Test on validation images
    val_images_path = "archive/val/images"
    image_files = [f for f in os.listdir(val_images_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    multi_damage_images = []
    
    for img_file in image_files:
        img_path = os.path.join(val_images_path, img_file)
        
        # Run inference with low confidence to catch all detections
        results = model(img_path, conf=0.2)
        
        # Collect all detected classes
        detected_classes = []
        confidences = {}
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names[cls]
                    
                    if class_name not in detected_classes:
                        detected_classes.append(class_name)
                        confidences[class_name] = conf
                    else:
                        # Keep highest confidence for each class
                        if conf > confidences[class_name]:
                            confidences[class_name] = conf
        
        # Check if this image has multiple damage types
        if len(detected_classes) > 1:
            multi_damage_images.append({
                'filename': img_file,
                'damages': detected_classes,
                'confidences': confidences
            })
    
    # Print results
    print(f"Found {len(multi_damage_images)} images with multiple damage types:\n")
    
    for i, img_data in enumerate(multi_damage_images, 1):
        print(f"{i}. {img_data['filename']}")
        for damage in img_data['damages']:
            conf = img_data['confidences'][damage]
            print(f"   - {damage}: {conf:.2f} confidence")
        print()
    
    # Specifically look for scratch + dent + lamp broken combinations
    print("=== SPECIFIC COMBINATIONS ===")
    
    scratch_dent_lamp = []
    scratch_dent = []
    scratch_lamp = []
    dent_lamp = []
    
    for img_data in multi_damage_images:
        damages = img_data['damages']
        
        if 'scratch' in damages and 'dent' in damages and 'lamp broken' in damages:
            scratch_dent_lamp.append(img_data['filename'])
        elif 'scratch' in damages and 'dent' in damages:
            scratch_dent.append(img_data['filename'])
        elif 'scratch' in damages and 'lamp broken' in damages:
            scratch_lamp.append(img_data['filename'])
        elif 'dent' in damages and 'lamp broken' in damages:
            dent_lamp.append(img_data['filename'])
    
    print(f"Scratch + Dent + Lamp broken: {scratch_dent_lamp}")
    print(f"Scratch + Dent: {scratch_dent}")
    print(f"Scratch + Lamp broken: {scratch_lamp}")
    print(f"Dent + Lamp broken: {dent_lamp}")

if __name__ == "__main__":
    find_multiple_damages()
