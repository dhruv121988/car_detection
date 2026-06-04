import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_training():
    print("=== ANALYZING TRAINING PROGRESS ===")
    
    # Check if results.csv exists
    results_path = "runs/detect/train3/results.csv"
    print(f"Results file: {results_path}")
    print(f"Results file exists: {os.path.exists(results_path)}")
    
    if os.path.exists(results_path):
        try:
            # Read the results
            df = pd.read_csv(results_path)
            print(f"Number of epochs completed: {len(df)}")
            print(f"Columns: {list(df.columns)}")
            
            if len(df) > 0:
                # Show final metrics
                final_epoch = df.iloc[-1]
                print(f"\n=== FINAL METRICS ===")
                print(f"Precision: {final_epoch.get('metrics/precision(B)', 'N/A'):.3f}")
                print(f"Recall: {final_epoch.get('metrics/recall(B)', 'N/A'):.3f}")
                print(f"mAP50: {final_epoch.get('metrics/mAP50(B)', 'N/A'):.3f}")
                print(f"mAP50-95: {final_epoch.get('metrics/mAP50-95(B)', 'N/A'):.3f}")
                
                # Show progress
                print(f"\n=== TRAINING PROGRESS ===")
                print("Epoch | Precision | Recall | mAP50")
                print("-" * 35)
                for i, row in df.iterrows():
                    epoch = i + 1
                    precision = row.get('metrics/precision(B)', 0)
                    recall = row.get('metrics/recall(B)', 0)
                    map50 = row.get('metrics/mAP50(B)', 0)
                    print(f"{epoch:5d} | {precision:9.3f} | {recall:6.3f} | {map50:6.3f}")
                
                # Check if training is improving
                if len(df) >= 2:
                    first_map = df.iloc[0].get('metrics/mAP50(B)', 0)
                    last_map = df.iloc[-1].get('metrics/mAP50(B)', 0)
                    improvement = last_map - first_map
                    print(f"\n=== IMPROVEMENT ===")
                    print(f"Initial mAP50: {first_map:.3f}")
                    print(f"Final mAP50: {last_map:.3f}")
                    print(f"Improvement: {improvement:+.3f}")
                    
                    if improvement < 0.01:
                        print("⚠️  Training may not be improving significantly")
                    else:
                        print("✅ Training is improving")
                
        except Exception as e:
            print(f"Error reading results: {str(e)}")
    else:
        print("❌ No training results found")
        print("Possible issues:")
        print("- Training didn't complete")
        print("- Training failed to save results")
        print("- Wrong training directory")
    
    # Check other training runs
    print(f"\n=== OTHER TRAINING RUNS ===")
    runs_dir = "runs/detect"
    if os.path.exists(runs_dir):
        runs = [d for d in os.listdir(runs_dir) if d.startswith('train')]
        print(f"Found training runs: {runs}")
        
        for run in runs:
            weights_path = f"{runs_dir}/{run}/weights/best.pt"
            if os.path.exists(weights_path):
                size = os.path.getsize(weights_path) / (1024*1024)  # MB
                print(f"  {run}: {size:.1f}MB")

if __name__ == "__main__":
    analyze_training()
