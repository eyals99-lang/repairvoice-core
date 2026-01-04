import os
import torch
from voicefixer import VoiceFixer
from tqdm import tqdm

# --- הגדרת נתיבים ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
INPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'restored')

def repair_files():
    # 1. יצירת תיקיית פלט
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Loading VoiceFixer model... (this might take a minute)")
    # בדיקה אם יש GPU זמין, אחרת משתמשים ב-CPU
    use_cuda = torch.cuda.is_available()
    device_name = "GPU" if use_cuda else "CPU"
    print(f"Running on: {device_name}")

    # טעינת המודל (יוריד משקלים מהאינטרנט בפעם הראשונה)
    vf = VoiceFixer() 

    # חיפוש קבצים שבורים
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.wav')]
    
    if not files:
        print("No broken files found to repair!")
        return

    print(f"Found {len(files)} files. Starting restoration...")

    for filename in tqdm(files):
        in_path = os.path.join(INPUT_DIR, filename)
        out_path = os.path.join(OUTPUT_DIR, f"fixed_{filename}")
        
        # --- ביצוע התיקון ---
        # mode 0: מודל אוטומטי לתיקון כללי (רעש + הדהוד)
        vf.restore(input=in_path, 
                   output=out_path, 
                   cuda=use_cuda, 
                   mode=0) 
                   
    print(f"Done! Results saved in {OUTPUT_DIR}")

if __name__ == "__main__":
    repair_files()