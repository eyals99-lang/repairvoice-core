# שימוש ב-Image רשמי של PyTorch עם תמיכה ב-CUDA (עבור NVIDIA GPUs)
# גרסה עדכנית יותר התומכת בפיצ'רים החדשים של VoiceFixer
FROM pytorch/pytorch:2.1.2-cuda11.8-cudnn8-runtime

# התקנת ספריות מערכת לעיבוד אודיו (חובה עבור librosa/soundfile)
#RUN apt-get update && apt-get install -y \
#    libsndfile1 \
#    ffmpeg \
#    git \
#    && rm -rf /var/lib/apt/lists/*

# הגדרת תיקיית העבודה
WORKDIR /app

# העתקת קובץ הדרישות והתקנת חבילות Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --upgrade --upgrade-strategy only-if-needed

# העתקת קוד המקור
COPY . .

# ברירת מחדל: הרצת shell
CMD ["/bin/bash"]

FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# 🔴 חייב לבוא לפני pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        make \
        libsndfile1 \
        ffmpeg \
        git \
        tzdata && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
