# --------------------------------------------------------------
# extract_keypoints.py
# --------------------------------------------------------------
import cv2
import numpy as np
import mediapipe as mp
from pathlib import Path
from tqdm import tqdm

# ------------------- CONFIG -----------------------------------
BASE_PATH = Path("/Users/macbookair/Desktop/Video_RSL_UzSL/signer01")

top_100_words = ['дом', 'школа', 'улица', 'дверь', 'стол', 'стул', 'кровать', 'машина', 'поезд', 
                 'метро', 'корабль', 'мост', 'дождь', 'снег', 'ветер', 'зима', 'весна', 'день', 
                 'пожалуйста', 'здравствуйте', 'извините', 'нормально', 'быстро', 'вместе', 'большой', 
                 'маленький', 'новый', 'добрый', 'готовить', 'писать', 'помогать', 'играть', 'гулять', 
                 'искать', 'терять', 'физкультура', 'вставать', 'уходить', 'приносить', 'открывать', 
                 'закрывать', 'светлый', 'тёмный', 'чистый', 'телевизор', 'полный', 'пустой', 'конец', 
                 'начало', 'поздно', 'скоро', 'ресторан', 'завод', 'церковь', 'базар', 'шоколад', 
                 'гостиница', 'книга', 'бумага', 'занавеска', 'одежда', 'обувь', 'носки', 'перчатки', 
                 'шапка', 'банковская_карта', 'хлеб', 'тарелка', 'холодильник', 'интернет', 'музыка', 
                 'ответ', 'земля', 'трава', 'камень', 'собака', 'кошка', 'корова', 'лошадь', 'овца', 
                 'свинья', 'картошка', 'морковь', 'капуста', 'помидор', 'огурец', 'чеснок', 'грибы', 
                 'сливочное_масло', 'стакан', 'футбол', 'читаю', 'подсолнечное_масло', 'мыло', 'подушка', 
                 'кролик', 'убираю', 'нахожу', 'грязный', 'рюкзак']

# MediaPipe settings (identical to your original code)
MP_CONFIDENCE = 0.5
POSE_REMOVE_IDX = [0,1,2,3,4,5,6,7,8,9,10,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]

# ------------------- MEDIA-PIPE INITIALISATION ---------------
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    min_detection_confidence=MP_CONFIDENCE,
    min_tracking_confidence=MP_CONFIDENCE,
    static_image_mode=False
)

# ------------------- HELPERS ---------------------------------
def detect_landmarks(frame):
    """Return processed frame + MediaPipe results (pose visibility zeroed)."""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb.flags.writeable = False
    results = holistic.process(rgb)
    rgb.flags.writeable = True

    # Zero visibility of unwanted pose points
    if results.pose_landmarks:
        for i in POSE_REMOVE_IDX:
            results.pose_landmarks.landmark[i].visibility = 0.0
    return results

def extract_vector(results):
    """Flatten exactly as in your collector (face-pose-rh-lh)."""
    pose = np.array([[lm.x, lm.y, lm.z, lm.visibility]
                     for lm in results.pose_landmarks.landmark]).flatten() \
           if results.pose_landmarks else np.zeros(33*4)

    face = np.array([[lm.x, lm.y, lm.z]
                     for lm in results.face_landmarks.landmark]).flatten() \
           if results.face_landmarks else np.zeros(468*3)

    rh = np.array([[lm.x, lm.y, lm.z]
                   for lm in results.right_hand_landmarks.landmark]).flatten() \
         if results.right_hand_landmarks else np.zeros(21*3)

    lh = np.array([[lm.x, lm.y, lm.z]
                   for lm in results.left_hand_landmarks.landmark]).flatten() \
         if results.left_hand_landmarks else np.zeros(21*3)

    return np.concatenate([face, pose, rh, lh])

# ------------------- MAIN PROCESSING -------------------------
def process_video(video_path: Path, landmark_dir: Path):
    """Read video → write one .npy per frame into landmark_dir."""
    landmark_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Warning: Could not open {video_path}")
        return

    frame_idx = 0
    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                desc=f"{video_path.parent.name}/{video_path.name}",
                leave=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detect_landmarks(frame)
        vec = extract_vector(results)

        np.save(landmark_dir / f"frame-{frame_idx:02d}.npy", vec)
        frame_idx += 1
        pbar.update(1)

    cap.release()
    pbar.close()

# ------------------- WALK THROUGH DATASET --------------------
def main():
    for word in top_100_words:
        word_dir = BASE_PATH / word
        if not word_dir.is_dir():
            print(f"Warning: Missing word folder: {word_dir}")
            continue

        video_base = word_dir / "videos"
        lm_base    = word_dir / "landmarks"

        for rep_folder in video_base.iterdir():
            if not rep_folder.is_dir() or not rep_folder.name.startswith("rep-"):
                continue

            video_file = rep_folder / "video.mp4"
            if not video_file.is_file():
                print(f"Warning: No video.mp4 in {rep_folder}")
                continue

            lm_rep_dir = lm_base / rep_folder.name
            # Skip if already done (all .npy files exist)
            expected_frames = int(cv2.VideoCapture(str(video_file)).get(cv2.CAP_PROP_FRAME_COUNT))
            existing = len(list(lm_rep_dir.glob("frame-*.npy"))) if lm_rep_dir.exists() else 0
            if existing == expected_frames:
                print(f"Skipping {word}/{rep_folder.name} (already extracted)")
                continue

            process_video(video_file, lm_rep_dir)

    print("\n=== ALL DONE ===")

if __name__ == "__main__":
    main()