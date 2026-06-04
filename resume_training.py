from ultralytics import YOLO

def resume_training():
    print("=== RESUMING TRAINING FROM EPOCH 7 ===")
    
    # Load the partially trained model
    model = YOLO("runs/detect/train3/weights/last.pt")
    
    # Resume training for remaining epochs (50 - 7 = 43 more epochs)
    model.train(
        data="archive/data.yaml",
        epochs=50,  # Total epochs
        imgsz=640,
        batch=8,
        workers=2,
        resume=True  # This resumes from the checkpoint
    )

if __name__ == "__main__":
    resume_training()
