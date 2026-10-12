# Cloud Deployment Guide — PCB AI Inspection & Metrology Suite

This guide walks you step-by-step through deploying the **Industrial PCB AI Inspection Suite** to cloud platforms (**Render** and **Railway**) so your web dashboard and REST API are accessible publicly over the internet.

---

## 🚀 Option 1: Deploy to Render (Recommended Free-Tier)

Render provides free cloud hosting with automatic SSL, custom domains, and continuous deployment from GitHub.

### Method A: 1-Click Blueprint (Easiest)

We have included a [`render.yaml`](./render.yaml) file configured for instant deployment.

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "feat: configure cloud deployment"
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com/) and sign in.
   - Click **New +** in the top navigation and select **Blueprint**.
   - Connect your GitHub repository.
   - Render reads `render.yaml` automatically and creates the service.
   - Click **Apply**.

3. **Access Your Live Dashboard**:
   - Render will build the container and provide a live URL:
     `https://pcb-ai-inspection.onrender.com`
   - Open that URL in your browser to view the Inspection Studio, Metrology Engine, and Photometric 3D Studio!

---

### Method B: Manual Web Service Setup on Render

If you prefer setting it up manually without Blueprint:

1. In Render Dashboard, click **New +** → **Web Service**.
2. Connect your GitHub repository.
3. Configure the settings:
   - **Name**: `pcb-ai-inspection`
   - **Region**: Choose the closest region (e.g., Oregon or Frankfurt).
   - **Language / Runtime**: **Docker** (Recommended, uses root [`Dockerfile`](./Dockerfile)).
   - **Plan**: **Free**.
4. In **Environment Variables**, add:
   - `PCB_AOI_ENV` = `production`
   - `PCB_AOI_REQUIRE_API_KEY` = `0`
   - `PCB_AOI_USE_DEPTH_MODEL` = `0`
   - `LOG_LEVEL` = `INFO`
5. Click **Create Web Service**.
6. Render builds the Docker image and runs health checks against `/health`.

---

## 🚆 Option 2: Deploy to Railway

Railway offers rapid deployment, automatic HTTPS domains, and zero-configuration Docker support.

### Deploying via Railway Dashboard:

1. **Push your repository to GitHub** (same as above).
2. Go to [railway.app](https://railway.app/) and log in with GitHub.
3. Click **+ New Project** → **Deploy from GitHub repo**.
4. Select your `pcb-image-processing` repository.
5. Railway detects [`railway.toml`](./railway.toml) and [`Dockerfile`](./Dockerfile) automatically.
6. Once deployed, click on the service card:
   - Go to **Settings** → **Networking** → Click **Generate Domain**.
   - Your public URL will look like: `https://<service-name>.up.railway.app`.

---

## 📷 Connecting the Camera Client (Laptop A) to Cloud

Once your server is deployed on Render or Railway, you can transmit live inspection frames from any laptop or edge camera directly to your cloud URL:

```bash
# On Laptop A (Camera Node):
python client/capture_and_send.py https://<YOUR_DEPLOYED_URL>/inspect
```

Or set the environment variable:
```powershell
$env:PCB_AOI_SERVER_URL="https://<YOUR_DEPLOYED_URL>/inspect"
python client/capture_and_send.py
```

---

## 🌐 Public REST API Endpoints

Once deployed, the following endpoints are available at your cloud URL:

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Main PCB Inspection Dashboard |
| `/photometric-studio` | `GET` | 3D Photometric Stereo & Solder Profiler Studio |
| `/xray-studio` | `GET` | 3D X-Ray Laminography & BGA Void Analyzer |
| `/health` | `GET` | Server liveness & pipeline module status |
| `/inspect` | `POST` | Inspect PCB image (multipart file upload or JSON test board serial) |
| `/cfx/telemetry` | `GET` | Industry 4.0 IPC-CFX-2591 telemetry feed |
| `/audit/logs` | `GET` | ISO 9001:2015 audit records with SHA-256 hashes |
| `/api/components` | `GET` | Component footprints and inspection ROIs |

---

## ⚙️ Environment Variables Reference

| Variable | Default | Purpose |
|---|---|---|
| `PORT` | `8000` | Port listened to by Uvicorn (Render & Railway inject this automatically) |
| `PCB_AOI_ENV` | `development` | Environment mode (`development` or `production`) |
| `PCB_AOI_REQUIRE_API_KEY` | `0` | Set `1` to require `X-API-Key` header on endpoints |
| `PCB_AOI_API_KEY` | *(empty)* | Secret API key if authentication is required |
| `PCB_AOI_USE_DEPTH_MODEL` | `0` | Set `1` to enable heavy HuggingFace Depth-Anything-V2 Small model |
| `LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
