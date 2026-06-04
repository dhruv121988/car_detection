from ultralytics import YOLO
import os
import yaml

def test_training_setup():
    print("=== TESTING TRAINING SETUP ===")
    
    # Check data.yaml file
    data_yaml_path = "archive/data.yaml"
    print(f"Data YAML path: {data_yaml_path}")
    print(f"Data YAML exists: {os.path.exists(data_yaml_path)}")
    
    if os.path.exists(data_yaml_path):
        with open(data_yaml_path, 'r') as f:
            data_config = yaml.safe_load(f)
            print(f"Data config: {data_config}")
    
    # Check training data directories
    train_dir = "archive/train/images"
    val_dir = "archive/val/images"
    
    print(f"\nTrain images directory: {train_dir}")
    print(f"Train directory exists: {os.path.exists(train_dir)}")
    if os.path.exists(train_dir):
        train_images = [f for f in os.listdir(train_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
        print(f"Number of training images: {len(train_images)}")
        if train_images:
            print(f"Sample training images: {train_images[:3]}")
    
    print(f"\nVal images directory: {val_dir}")
    print(f"Val directory exists: {os.path.exists(val_dir)}")
    if os.path.exists(val_dir):
        val_images = [f for f in os.listdir(val_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
        print(f"Number of validation images: {len(val_images)}")
        if val_images:
            print(f"Sample validation images: {val_images[:3]}")
    
    # Check label directories
    train_labels_dir = "archive/train/labels"
    val_labels_dir = "archive/val/labels"
    
    print(f"\nTrain labels directory: {train_labels_dir}")
    print(f"Train labels directory exists: {os.path.exists(train_labels_dir)}")
    if os.path.exists(train_labels_dir):
        train_labels = [f for f in os.listdir(train_labels_dir) if f.endswith('.txt')]
        print(f"Number of training label files: {len(train_labels)}")
    
    print(f"\nVal labels directory: {val_labels_dir}")
    print(f"Val labels directory exists: {os.path.exists(val_labels_dir)}")
    if os.path.exists(val_labels_dir):
        val_labels = [f for f in os.listdir(val_labels_dir) if f.endswith('.txt')]
        print(f"Number of validation label files: {len(val_labels)}")
    
    # Test a single training step
    print("\n=== TESTING MODEL TRAINING INITIALIZATION ===")
    try:
        model = YOLO("yolov8n.pt")
        print("Base model loaded successfully!")
        
        # Test if training can start (but don't actually train)
        print("Testing training configuration...")
        print("This would start training if run:")
        print(f"model.train(data='{data_yaml_path}', epochs=1, imgsz=640, batch=8, workers=2)")
        
    except Exception as e:
        print(f"Error in training setup: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_training_setup()
