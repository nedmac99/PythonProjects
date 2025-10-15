import streamlit as st
import cv2
import os
import numpy as np
from mtcnn import MTCNN
from deepface import DeepFace
from pathlib import Path
from scipy.spatial.distance import cosine
from datetime import datetime
from PIL import Image

# ----------------------------------------
# Auto-refresh every 3 seconds
# ----------------------------------------
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=3000, key="refresh")

# ----------------------------------------
# Setup paths and thresholds
# ----------------------------------------
db_path = Path(__file__).parent / "faces"
db_path.mkdir(exist_ok=True)

cosine_threshold = 0.63
confidence_threshold = 0.95

# ----------------------------------------
# Load embeddings
# ----------------------------------------
st.sidebar.header("Configuration")
st.sidebar.info("Ensure your known face images are saved in the 'faces/' folder.")

st.write("Loading known faces...")
known_embeddings = []
known_names = []

for file in os.listdir(db_path):
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        img_path = str(db_path / file)
        emb = DeepFace.represent(
            img_path=img_path, model_name="VGG-Face", enforce_detection=True
        )[0]["embedding"]
        emb = emb / np.linalg.norm(emb)
        known_embeddings.append(emb)
        known_names.append(os.path.splitext(file)[0])

st.success(f"✅ Loaded {len(known_names)} known face(s).")

# ----------------------------------------
# MTCNN detector and session state
# ----------------------------------------
detector = MTCNN()
if "attendance" not in st.session_state:
    st.session_state.attendance = {}

# ----------------------------------------
# UI
# ----------------------------------------
st.title("📸 Face Recognition Attendance System")
st.markdown(
    """
    This app:
    - Detects faces using **MTCNN**
    - Recognizes using **DeepFace (VGG-Face)**
    - Marks attendance automatically when a known face is seen
    """
)

img = st.camera_input("Camera Feed")

if img is not None:
    frame = Image.open(img)
    frame = np.array(frame)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    rgb_frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    detections = detector.detect_faces(rgb_frame)

    for face in detections:
        if face.get("confidence", 0) < confidence_threshold:
            continue

        x, y, w, h = face["box"]
        x, y = max(0, x), max(0, y)
        face_img = frame_bgr[y:y + h, x:x + w]

        if face_img.size == 0:
            continue

        face_img = cv2.resize(face_img, (224, 224))
        emb = DeepFace.represent(
            img_path=face_img, model_name="VGG-Face", enforce_detection=False
        )[0]["embedding"]
        emb = emb / np.linalg.norm(emb)

        if known_embeddings:
            distances = [cosine(emb, k_emb) for k_emb in known_embeddings]
            min_idx = int(np.argmin(distances))
            min_dist = float(distances[min_idx])
            name = known_names[min_idx] if min_dist < cosine_threshold else "Unknown"
        else:
            name = "Unknown"

        # Mark attendance
        if name != "Unknown" and name not in st.session_state.attendance:
            st.session_state.attendance[name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        color = (0, 255, 0) if name != "Unknown" else (0, 255, 255)
        cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame_bgr, name, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    st.image(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB), channels="RGB")

# ----------------------------------------
# Attendance display
# ----------------------------------------
st.subheader("Attendance Records")
st.dataframe(st.session_state.attendance)


