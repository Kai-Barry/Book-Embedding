# 🚀 Step-by-Step Unraid NAS Deployment Guide

This comprehensive guide will walk you through deploying the **Book-Embedding Engine** on your **Unraid NAS (12th Gen Intel i5)**.

---

## ⚡ Performance Summary on Intel 12th Gen i5 CPU
* **Cosine Similarity Speed**: $\approx 1.6\text{ms}$ across all 25,101 books using Intel AVX2 & VNNI instructions.
* **Memory Footprint**: $\approx 350\text{MB}$ RAM.
* **No Discrete GPU Needed**: Precomputed dense vectors allow instantaneous similarity discovery and weight tuning on pure CPU.

---

## 📋 Prerequisites
1. An active **Unraid Server** with Docker enabled.
2. The precomputed vector data files from this repository:
   * `data/vector_db/embeddings.npy`
   * `data/vector_db/book_index/`
   * `data/vector_db/coords_2d.npy`

---

## 📂 Step 1: Copy Precomputed Data to Your NAS

On your Unraid server (via SSH or the Unraid Dynamix File Manager / SMB Share), create the application folder and copy the `data` folder:

```bash
mkdir -p /mnt/user/appdata/book-embedding/data
mkdir -p /mnt/user/appdata/book-embedding/cache
```

Copy the repository `data/` folder from your desktop/local machine into `/mnt/user/appdata/book-embedding/data/`.

---

## 🛠️ Step 2: Choose Your Deployment Method

### Method A: Build from Source on Unraid with Docker Compose (Easiest)

If you have the **Docker Compose Manager** plugin installed in Unraid:

1. SSH into your Unraid server and clone the repository directly into appdata:
   ```bash
   cd /mnt/user/appdata
   git clone https://github.com/Kai-Barry/Book-Embedding.git book-embedding-app
   cd book-embedding-app
   ```
2. Copy your precomputed dataset into `./data`:
   ```bash
   # Ensure data files exist in /mnt/user/appdata/book-embedding-app/data/vector_db/
   ```
3. Set your preferred **Host Port** (e.g. `8501`, `8080`, `7860` so it doesn't conflict with other NAS containers) by creating a `.env` file:
   ```bash
   echo "HOST_PORT=8501" > .env
   ```
4. Build and start the container:
   ```bash
   docker compose up -d --build
   ```

---

### Method B: Native Unraid Docker Web UI (Using Template)

1. Copy the provided [`unraid-template.xml`](file:///d:/code/Book-Embedding/unraid-template.xml) to your Unraid flash drive:
   ```bash
   cp unraid-template.xml /boot/config/plugins/dockerMan/templates-user/my-Book-Embedding.xml
   ```
2. In the **Unraid Web GUI**:
   * Navigate to the **Docker** tab.
   * Scroll down and click **Add Container**.
   * Under the **Template** dropdown, select `my-Book-Embedding`.
   * **WebUI Port**: Set to any free port on your NAS (e.g. `8501`).
   * **App Data Path**: Ensure `/app/data` is mapped to `/mnt/user/appdata/book-embedding/data`.
   * **Model Cache Path**: Ensure `/root/.cache` is mapped to `/mnt/user/appdata/book-embedding/cache`.
   * Click **Apply**. Unraid will pull the image, map the ports, and start the engine.

---

### Method C: Manual One-Line Docker Run

From an SSH terminal on Unraid:

```bash
cd /mnt/user/appdata/book-embedding-app

# 1. Build the lightweight CPU image
docker build -t book-embedding:latest .

# 2. Run the container on your preferred port (e.g. 8501)
docker run -d \
  --name book-embedding \
  --restart unless-stopped \
  -p 8501:8000 \
  -e PORT=8000 \
  -e HOST=0.0.0.0 \
  -e DEVICE=cpu \
  -e OMP_NUM_THREADS=4 \
  -v /mnt/user/appdata/book-embedding/data:/app/data \
  -v /mnt/user/appdata/book-embedding/cache:/root/.cache \
  book-embedding:latest
```

---

## 🌐 Step 3: Accessing the Web Interface

Open any browser on your local network and visit:
```text
http://<YOUR-UNRAID-IP>:<YOUR-PORT>/
```
*Example:* `http://192.168.1.100:8501/`

---

## 🔧 Useful Maintenance Commands

* **View live logs:**
  ```bash
  docker logs -f book-embedding
  ```
* **Restart the container:**
  ```bash
  docker restart book-embedding
  ```
* **Update to latest code:**
  ```bash
  cd /mnt/user/appdata/book-embedding-app
  git pull origin main
  docker compose up -d --build
  ```

