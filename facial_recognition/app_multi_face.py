import cv2
import os
import numpy as np
from mtcnn import MTCNN
from deepface import DeepFace
from pathlib import Path
from scipy.spatial.distance import cosine
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
db_path = Path(__file__).parent / "faces"
cosine_threshold = 0.63
confidence_threshold = 0.95
detect_interval = 5
max_missed_frames = 10
embedding_refresh_interval = 10
recognition_smooth_frames = 3
iou_threshold = 0.3
remove_iou_threshold = 0.20
unknown_drop_frames = 3


# -----------------------------
# Helper: IoU
# -----------------------------
def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])
    interW = max(0, xB - xA)
    interH = max(0, yB - yA)
    interArea = interW * interH
    boxAArea = boxA[2] * boxA[3]
    boxBArea = boxB[2] * boxB[3]
    return interArea / float(boxAArea + boxBArea - interArea + 1e-6)


# -----------------------------
# Load known embeddings
# -----------------------------
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

print("Loaded embeddings for:", known_names)

# -----------------------------
# Initialize
# -----------------------------
attendance = set()  # keep only names seen once
trackers = []
frame_count = 0
cap = cv2.VideoCapture(0)
detector = MTCNN()
print("Starting camera... Press 'q' to quit.")

# -----------------------------
# Main loop
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    h_frame, w_frame = frame.shape[:2]
    updated_trackers = []

    # --- Update trackers ---
    for t in trackers:
        success, bbox = t["tracker"].update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = min(x + w, w_frame), min(y + h, h_frame)
            if x2 - x1 <= 0 or y2 - y1 <= 0:
                t["missed_frames"] += 1
                if t["missed_frames"] < max_missed_frames:
                    updated_trackers.append(t)
                continue

            t["bbox"] = (x1, y1, x2 - x1, y2 - y1)
            t["missed_frames"] = 0

            # recompute embedding periodically
            if frame_count % embedding_refresh_interval == 0:
                face_img = frame[y1:y2, x1:x2]
                if face_img.size > 0:
                    face_img = cv2.resize(face_img, (224, 224))
                    face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                    emb = DeepFace.represent(
                        img_path=face_img_rgb,
                        model_name="VGG-Face",
                        enforce_detection=False,
                    )[0]["embedding"]
                    t["embedding"] = emb / np.linalg.norm(emb)

            # compare to known faces
            distances = [cosine(t["embedding"], k_emb) for k_emb in known_embeddings]
            min_idx = int(np.argmin(distances))
            min_dist = float(distances[min_idx])
            candidate = (
                known_names[min_idx] if min_dist < cosine_threshold else "Unknown"
            )

            if candidate != t.get("last_candidate", "Unknown"):
                t["consecutive_frames"] = 1
                t["last_candidate"] = candidate
            else:
                t["consecutive_frames"] = t.get("consecutive_frames", 0) + 1

            # confirm recognition
            if t["consecutive_frames"] >= recognition_smooth_frames:
                prev_name = t.get("name", "Unknown")
                if prev_name != candidate:
                    t["name"] = candidate
                    if candidate != "Unknown" and candidate not in attendance:
                        attendance.add(candidate)
                        print(
                            f"[ATTENDANCE] {candidate} recognized at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        )

            color = (
                (0, 255, 0) if t.get("name", "Unknown") != "Unknown" else (0, 255, 255)
            )
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                t.get("name", "Unknown"),
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )

            updated_trackers.append(t)
        else:
            t["missed_frames"] += 1
            if t["missed_frames"] < max_missed_frames:
                updated_trackers.append(t)

    trackers = updated_trackers

    # --- Run face detection every N frames ---
    if frame_count % detect_interval == 0:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = detector.detect_faces(rgb_frame)

        det_boxes = []
        for face in detections:
            if face.get("confidence", 0) < confidence_threshold:
                continue
            x, y, w, h = face["box"]
            x1, y1 = max(0, x), max(0, y)
            x2, y2 = min(x + w, w_frame), min(y + h, h_frame)
            ww, hh = x2 - x1, y2 - y1
            if ww <= 0 or hh <= 0 or ww < 40 or hh < 40:
                continue
            det_boxes.append((x1, y1, ww, hh))

        # remove inactive trackers
        kept = []
        for t in trackers:
            bbox_t = t.get("bbox")
            if bbox_t is None:
                continue
            if len(det_boxes) == 0:
                kept.append(t)
                continue

            max_iou = max([iou(bbox_t, db) for db in det_boxes]) if det_boxes else 0
            if max_iou < remove_iou_threshold:
                continue
            if t.get("name", "Unknown") == "Unknown":
                t["unknown_count"] = t.get("unknown_count", 0) + 1
            else:
                t["unknown_count"] = 0
            if t.get("unknown_count", 0) >= unknown_drop_frames:
                continue
            kept.append(t)

        trackers = kept

        # add new trackers for new detections
        for db in det_boxes:
            duplicate = any(
                "bbox" in t and iou(t["bbox"], db) > iou_threshold for t in trackers
            )
            if duplicate:
                continue

            x1, y1, w1, h1 = db
            face_img = frame[y1 : y1 + h1, x1 : x1 + w1]
            if face_img.size == 0:
                continue
            face_img = cv2.resize(face_img, (224, 224))
            face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

            emb = DeepFace.represent(
                img_path=face_img_rgb, model_name="VGG-Face", enforce_detection=False
            )[0]["embedding"]
            emb = emb / np.linalg.norm(emb)

            distances = (
                [cosine(emb, k_emb) for k_emb in known_embeddings]
                if known_embeddings
                else [1.0]
            )
            min_idx = int(np.argmin(distances)) if distances else 0
            min_dist = float(distances[min_idx]) if distances else 1.0
            name = known_names[min_idx] if min_dist < cosine_threshold else "Unknown"

            tracker = cv2.legacy.TrackerCSRT_create()
            tracker.init(frame, (x1, y1, w1, h1))
            trackers.append(
                {
                    "tracker": tracker,
                    "name": "Unknown",
                    "embedding": emb,
                    "missed_frames": 0,
                    "bbox": (x1, y1, w1, h1),
                    "last_candidate": name,
                    "consecutive_frames": 1,
                    "unknown_count": 0,
                }
            )

    # --- UI ---
    if len(trackers) == 0:
        cv2.putText(
            frame,
            "No face detected",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

    cv2.imshow("Face Recognition Attendance System", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup
cap.release()
cv2.destroyAllWindows()

print("\nFinal attendance:")
for name in attendance:
    print(f"- {name}")
