import os
import subprocess
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
# 2. Helper
# ------------------------------------------------------------
def output_path_for_index(idx: int) -> str:
    return f"video{'' if idx == 1 else idx}.mp4"

# ------------------------------------------------------------
# 3. Main loop
# ------------------------------------------------------------
for word in top_100_words:
    videos_dir = base_path / word / "videos"
    if not videos_dir.is_dir():
        print(f"[SKIP] {videos_dir} does not exist")
        continue

    src_files = sorted([p for p in videos_dir.iterdir() if p.suffix.lower() == ".mp4"])
    if not src_files:
        print(f"[EMPTY] No .mp4 in {videos_dir}")
        continue

    print(f"\n=== {word} – {len(src_files)} file(s) ===")
    os.chdir(videos_dir)

    for idx, src in enumerate(src_files, start=1):
        out_name = output_path_for_index(idx)
        out_path = videos_dir / out_name

        # ------------------------------------------------------------
        # ffmpeg command – uses libopenh264 (available in your build)
        # ------------------------------------------------------------
        cmd = [
            "ffmpeg",
            "-y",                     # overwrite
            "-i", str(src),

            # ----- video: lossless H.264 via OpenH264 ----------------
            "-c:v", "libopenh264",
            "-filter:v", "setpts=N/30/TB",   # exact 30.00000 fps
            "-r", "30",               # container rate

            # ----- audio --------------------------------------------
            "-an",                    # remove audio

            str(out_path)
        ]

        print(f"  [{idx}] {src.name} → {out_name}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"    ERROR: {result.stderr.strip()}")
        else:
            size_mb = out_path.stat().st_size / (1024 * 1024)
            print(f"    Done – {size_mb:.2f} MiB – exact 30 fps")