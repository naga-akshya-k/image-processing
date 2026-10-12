"""
Laptop A — Webcam Capture & Inspection Client
Team 6 - AI Deployment, API Server & Client UX

Captures live webcam feed from Laptop A, transmits frames to Laptop B or Cloud Server,
and renders the inspection overlay locally.
"""

import os
import sys
import time
import base64
import requests
import cv2
import numpy as np

# Configurable server endpoint (defaults to local or cloud URL)
DEFAULT_SERVER_URL = os.getenv("PCB_AOI_SERVER_URL", "http://localhost:8000/inspect")
CLIENT_API_KEY = os.getenv("PCB_AOI_API_KEY", "").strip()
CLIENT_MAX_RETRIES = max(1, int(os.getenv("PCB_AOI_CLIENT_MAX_RETRIES", "3")))
CLIENT_TIMEOUT_SECONDS = float(os.getenv("PCB_AOI_CLIENT_TIMEOUT_SECONDS", "15"))
CLIENT_RETRY_BASE_SECONDS = float(os.getenv("PCB_AOI_CLIENT_RETRY_BASE_SECONDS", "1.5"))


def build_request_headers():
    headers = {"Accept": "application/json"}
    if CLIENT_API_KEY:
        headers["X-API-Key"] = CLIENT_API_KEY
    return headers


def send_image_for_inspection(image_bgr, server_url=DEFAULT_SERVER_URL):
    success, img_encoded = cv2.imencode(".png", image_bgr)
    if not success:
        print("[ERROR] Failed to encode image for upload.")
        return None

    files = {"file": ("inspection_board.png", img_encoded.tobytes(), "image/png")}
    headers = build_request_headers()

    for attempt in range(1, CLIENT_MAX_RETRIES + 1):
        try:
            resp = requests.post(
                server_url,
                files=files,
                headers=headers,
                timeout=CLIENT_TIMEOUT_SECONDS
            )

            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 503:
                try:
                    payload = resp.json()
                except Exception:
                    payload = {}
                if payload.get("detail") == "reference_not_set":
                    print("[ERROR] Server returned 503: Reference Board Not Set!")
                    return None
                if attempt < CLIENT_MAX_RETRIES:
                    delay = CLIENT_RETRY_BASE_SECONDS * attempt
                    print(f"[WARNING] Server unavailable on attempt {attempt}. Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    continue
                print(f"[ERROR] HTTP 503: {resp.text}")
                return None
            elif resp.status_code == 401:
                print("[ERROR] Server rejected the API key (401 Unauthorized).")
                return None
            elif resp.status_code == 422:
                print(f"[ERROR] Server returned 422: Validation or Alignment failed: {resp.text}")
                return None
            elif resp.status_code in {408, 429} or 500 <= resp.status_code <= 599:
                if attempt < CLIENT_MAX_RETRIES:
                    delay = CLIENT_RETRY_BASE_SECONDS * attempt
                    print(f"[WARNING] HTTP {resp.status_code} on attempt {attempt}. Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    continue
                print(f"[ERROR] HTTP {resp.status_code}: {resp.text}")
                return None
            else:
                print(f"[ERROR] HTTP {resp.status_code}: {resp.text}")
                return None

        except requests.exceptions.Timeout:
            if attempt < CLIENT_MAX_RETRIES:
                delay = CLIENT_RETRY_BASE_SECONDS * attempt
                print(f"[WARNING] Request timeout on attempt {attempt}. Retrying in {delay:.1f}s...")
                time.sleep(delay)
                continue
            print(f"[ERROR] Request timeout on final attempt {attempt}.")
            return None
        except requests.exceptions.RequestException as e:
            if attempt < CLIENT_MAX_RETRIES:
                delay = CLIENT_RETRY_BASE_SECONDS * attempt
                print(f"[WARNING] Connection error on attempt {attempt}: {e}. Retrying in {delay:.1f}s...")
                time.sleep(delay)
                continue
            print(f"[ERROR] Connection error: {e}")
            return None

    return None


def main():
    server_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SERVER_URL
    print("==================================================")
    print("  PCB AI INSPECTION CLIENT (CAMERA NODE)")
    print("==================================================")
    print(f"Target Server: {server_url}")
    print("Controls: Press SPACE to capture & inspect | Press 'q' to quit\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[WARNING] Could not open webcam index 0.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame from webcam.")
            break

        cv2.putText(frame, "PRESS SPACE TO INSPECT BOARD", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Inspection Camera Feed", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == 32:  # SPACE key
            print("[CLIENT] Capturing frame and sending to inspection server...")
            res = send_image_for_inspection(frame, server_url)
            if res:
                hi = res.get("health_index", 0.0)
                verdict = res.get("verdict", "UNKNOWN")
                latency = res.get("processing_time_ms", 0.0)
                print(f"[RESULT] Health Index: {hi:.3f} | Verdict: {verdict} | Latency: {latency:.1f} ms")

                if "overlay_image_b64" in res and res["overlay_image_b64"]:
                    img_bytes = base64.b64decode(res["overlay_image_b64"])
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    overlay_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    cv2.imshow("Inspection Result Overlay", overlay_bgr)
                    cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
