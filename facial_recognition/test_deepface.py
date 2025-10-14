from deepface import DeepFace
from pathlib import Path

file_path1 = Path(__file__).parent / "test_faces" / "burnie-burns.jpg"
file_path2 = Path(__file__).parent / "test_faces" / "ramsey-geoff.jpg"

result = DeepFace.verify(
    img1_path=file_path1,
    img2_path=file_path2
)

print(result)