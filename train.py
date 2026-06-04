from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")

    model.train(
        data=r"C:\Users\LENOVO\OneDrive\Desktop\car detection\archive\data.yaml",
        epochs=50,
        imgsz=640,
        batch=8,      # 👈 reduce (IMPORTANT)
        workers=2     # 👈 reduce
    )

if __name__ == "__main__":
    main()