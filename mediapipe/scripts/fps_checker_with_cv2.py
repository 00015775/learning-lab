import cv2
from pathlib import Path

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

base_path = Path("/Users/macbookair/Desktop/Video_RSL_UzSL/signer01")

# ------------------------------------------------------------
# 2. Helper – get frame count + declared FPS with OpenCV
# ------------------------------------------------------------
def get_video_info(video_path: Path):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return None, None

    # ---- count frames (reliable) --------------------------------
    frame_count = 0
    while True:
        ret, _ = cap.read()
        if not ret:
            break
        frame_count += 1

    # ---- declared FPS (CAP_PROP_FPS) -----------------------------
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    # some codecs return 0 → treat as unknown
    fps = fps if fps > 0 else None
    return frame_count, fps

# ------------------------------------------------------------
# 3. Main loop – scan every word folder
# ------------------------------------------------------------
for word in top_100_words:
    videos_dir = base_path / word / "videos"
    if not videos_dir.is_dir():
        continue

    # look only for the output files we created: video.mp4, video2.mp4, …
    out_files = sorted(
        p for p in videos_dir.iterdir()
        if p.name.startswith("video") and p.suffix.lower() == ".mp4"
    )

    if not out_files:
        continue

    print(f"\n=== {word} – {len(out_files)} file(s) ===")
    for vid in out_files:
        frames, fps = get_video_info(vid)
        if fps is None:
            fps_str = "???"
        else:
            fps_str = f"{fps:.5f}"   # show many decimals for exactness

        print(f"  {vid.name:12} →  {frames:4} frames  @  {fps_str} fps")