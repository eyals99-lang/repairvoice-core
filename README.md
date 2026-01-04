# RepairVoice Core Engine 🎙️✨

> **AI-Powered Speech Restoration & Enhancement System**

The core engine for **RepairVoice**: A startup dedicated to restoring broken, clipped, or noisy voice audio using advanced Generative AI models. The system utilizes a Hybrid Cloud-Edge architecture.

## 🚀 Current Status
This repository contains the **Backend Research Pipeline**:
1.  **Data Degradation:** Synthetic generation of "broken" data (noise, clipping, bandwidth limitation) from clean audio for training and benchmarking.
2.  **Restoration Engine:** Utilization of the **VoiceFixer** model (Neural Vocoder based) to repair and enhance audio.
3.  **Containerization:** A full Dockerized environment (PyTorch 2.1 + CUDA Support) to ensure reproducibility and compatibility.

---

## 🛠️ Prerequisites

* **Docker Desktop** installed and running.
* (Optional but recommended) **NVIDIA GPU** with updated drivers for hardware acceleration.
* At least one clean audio file (`.wav`) placed in the `data/raw` directory to get started.

---

## 🏃‍♂️ Quick Start

We use Docker to manage dependencies and versions.

### 1. Build the Environment
Build the Docker image (this may take a few minutes the first time):

```bash
docker build -t repairvoice-env .
