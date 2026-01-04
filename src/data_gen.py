import os
import glob
import numpy as np
import soundfile as sf
import librosa
from tqdm import tqdm

# --- תיקון: הגדרת נתיבים אבסולוטית מבוססת מיקום הסקריפט ---
# משיג את המיקום המדויק של הקובץ data_gen.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# עולה תיקייה אחת למעלה (לתיקיית השורש של הפרויקט) ואז נכנס ל-data
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

INPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
SAMPLE_RATE = 16000 
# -----------------------------------------------------------


def add_white_noise(audio, snr_db):
    """
    הוספת רעש לבן לפי יחס אות-לרעש (SNR) מבוקש
    """
    # חישוב עוצמת האות
    signal_power = np.mean(audio ** 2)
    # המרת SNR מ-dB לסקאלה לינארית
    snr_linear = 10 ** (snr_db / 10)
    # חישוב עוצמת הרעש הנדרשת
    noise_power = signal_power / snr_linear
    # יצירת הרעש
    noise = np.random.normal(0, np.sqrt(noise_power), audio.shape)
    return audio + noise

def simulate_clipping(audio, threshold=0.6):
    """
    דימוי של מיקרופון שנכנס לרוויה (דיסטורשן)
    """
    return np.clip(audio, -threshold, threshold)

def process_files():
    # יצירת תיקיית יעד אם לא קיימת
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # חיפוש קבצי WAV (אפשר להוסיף גם FLAC/MP3)
    files = glob.glob(os.path.join(INPUT_DIR, '*.wav'))
    
    print(f"Found {len(files)} files. Starting degradation process...")

    for file_path in tqdm(files):
        filename = os.path.basename(file_path)
        
        # 1. טעינת הקובץ והמרה למונו + 16kHz
        y, sr = librosa.load(file_path, sr=SAMPLE_RATE, mono=True)
        
        # 2. הוספת רעש (SNR של 10dB - רעש בינוני)
        y_noisy = add_white_noise(y, snr_db=10)
        
        # 3. הוספת דיסטורשן קל
        y_broken = simulate_clipping(y_noisy, threshold=0.7)
        
        # 4. שמירת הקובץ הפגום
        output_path = os.path.join(OUTPUT_DIR, f"broken_{filename}")
        sf.write(output_path, y_broken, SAMPLE_RATE)

if __name__ == "__main__":
    process_files()