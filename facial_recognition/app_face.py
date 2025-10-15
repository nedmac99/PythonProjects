import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np
from mtcnn import MTCNN
from deepface import DeepFace
from scipy.spatial.distance import cosine
from pathlib import Path
from datetime import datetime
import os

# -----------------------------
# Config
# -----------------------------
db_path = Path(__file__).parent / "faces"
db_path.mkdir(exist_ok=True)  # creates folder if it doesn't exist

cosine_threshold = 0.63
confidence_threshold = 0.95
recognition_smooth_frames = 3

# -----------------------------
# Load known embeddings
# -----------------------------
known_embeddings = []
known_names = []

for file in os.listdir(db_path):
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        img_path = str(db_path / file)
        emb = DeepFace.represent(img_path=img_path, model_name="VGG-Face", enforce_detection=True)[0]["embedding"]
        emb = emb / np.linalg.norm(emb)
        known_embeddings.append(emb)
        known_names.append(file.split(".")[0])

# -----------------------------
# Helper: IoU
# -----------------------------
def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = boxA[2] * boxA[3]
    boxBArea = boxB[2] * boxB[3]
    return interArea / float(boxAArea + boxBArea - interArea + 1e-6)

# -----------------------------
# Face recognition transformer
# -----------------------------
class FaceRecognizer(VideoTransformerBase):
    def __init__(self):
        self.detector = MTCNN()
        self.trackers = []
        self.frame_count = 0
        self.attendance = {}
        self.recognition_smooth_frames = recognition_smooth_frames

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1
        h_frame, w_frame = img.shape[:2]

        # --- Detect faces every frame ---
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detections = self.detector.detect_faces(rgb_frame)

        for face in detections:
            if face.get("confidence", 0) < confidence_threshold:
                continue

            x, y, w, h = face["box"]
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = min(x + w, w_frame), min(y + h, h_frame)
            face_img = img[y1:y2, x1:x2]
            if face_img.size == 0:
                continue
            face_img_rgb = cv2.cvtColor(cv2.resize(face_img, (224, 224)), cv2.COLOR_BGR2RGB)
            emb = DeepFace.represent(img_path=face_img_rgb, model_name="VGG-Face", enforce_detection=False)[0]["embedding"]
            emb = emb / np.linalg.norm(emb)

            # Compare with known faces
            if known_embeddings:
                distances = [cosine(emb, k_emb) for k_emb in known_embeddings]
                min_idx = int(np.argmin(distances))
                min_dist = float(distances[min_idx])
                name = known_names[min_idx] if min_dist < cosine_threshold else "Unknown"
            else:
                name = "Unknown"

            # Add attendance
            if name != "Unknown" and name not in self.attendance:
                self.attendance[name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Draw rectangle and name
            color = (0, 255, 0) if name != "Unknown" else (0, 255, 255)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        return img

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Live Face Recognition Attendance System")
webrtc_streamer(key="face-recog", video_transformer_factory=FaceRecognizer)








