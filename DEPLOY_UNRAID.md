# 🚀 Unraid & Docker Deployment Guide

This guide walks you through deploying the **Book-Embedding Engine** on your **Unraid NAS (12th Gen Intel i5)**.

---

## ⚡ Intel 12th Gen CPU Performance Highlights
* **Pure CPU Vector Dot Products**: $\approx 1.6\text{ms}$ across all 25,101 books using Intel AVX2 instructions.
* **RAM Footprint**: $\approx 350\text{MB}$ in-memory matrix.
* **Zero GPU Required**: Precomputed 1024-dim dense vectors allow instantaneous similarity search and slider tuning without needing an NVIDIA card.

---

## Option 1: Unraid Docker Template (Recommended)

1. **Copy the Template**:
   Copy [`unraid-template.xml`](file:///d:/code/Book-Embedding/unraid-template.xml) to your Unraid flash drive:
   ```bash
   /boot/config/plugins/dockerMan/templates-user/my-Book-Embedding.xml
   ```
2. **Add Container via Unraid WebUI**:
   * Go to the **Docker** tab in Unraid.
   * Click **Add Container** at the bottom.
   * Select the **Template**: `my-Book-Embedding`.
   * **Configure Port**: Set the `WebUI Port` to any port not currently used on your NAS (e.g. `8501`, `8080`, `7860`, or `8000`).
   * **Set AppData Path**: Confirm `/mnt/user/appdata/book-embedding/data`.
   * Click **Apply**.

---

## Option 2: Docker Compose (via Unraid Docker Compose Manager)

If you have the **Compose Manager** plugin installed in Unraid:

1. Clone or copy this repository to `/mnt/user/appdata/book-embedding`:
   ```bash
   git clone git@github.com:Kai-Barry/Book-Embedding.git /mnt/user/appdata/book-embedding
   cd /mnt/user/appdata/book-embedding
   ```
2. Set your preferred host port in a `.env` file (optional, defaults to `8000`):
   ```bash
   HOST_PORT=8501
   ```
3. Start the stack:
   ```bash
   docker compose up -d --build
   ```

---

## Option 3: Manual `docker run` Command

```bash
docker build -t book-embedding:latest .

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

## 🔍 Verification & Health Check

After launching, open your browser and navigate to:
```text
http://<UNRAID-IP>:<YOUR-CHOSEN-PORT>/
```
(e.g., `http://192.168.1.50:8501/`)
