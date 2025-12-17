import subprocess
from pathlib import Path
from typing import List

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
# 2. Helper – get FPS with ffprobe
# ------------------------------------------------------------
def get_fps(video_path: Path) -> str:
    """Return the container FPS as a string, e.g. '30/1' → '30.00000'."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate",
        "-of", "csv=p=0",
        str(video_path)
    ]
    try:
        out = subprocess.check_output(cmd, text=True).strip()
        # out is something like "30/1"
        num, den = map(int, out.split("/"))
        return f"{num/den:.5f}"
    except Exception as e:
        return f"ERROR ({e})"

# ------------------------------------------------------------
# 3. Main – scan every word folder
# ------------------------------------------------------------
# Print header
print(f"{'WORD':<12} {'VIDEO':<20} {'FPS'}")
print("-" * 12 + " " + "-" * 20 + " " + "-" * 10)

for word in top_100_words:
    videos_dir = base_path / word / "videos"
    if not videos_dir.is_dir():
        continue

    # Find all *output* files: video.mp4, video2.mp4, video3.mp4, …
    video_files = sorted(
        p for p in videos_dir.iterdir()
        if p.is_file() and p.name.startswith("video") and p.suffix.lower() == ".mp4"
    )

    if not video_files:
        continue

    for vid in video_files:
        fps = get_fps(vid)
        print(f"{word:<12} {vid.name:<20} {fps}")