import os
import subprocess
import sys
from pathlib import Path
import cv2

# ----------------------------------------------------------------------
def get_info_cv2(video_path):
    """Return (frame_count, fps) using OpenCV, or (None, None) on error."""
    if not os.path.exists(video_path):
        return None, None

    cap = cv2.VideoCapture(video_path) # Replace with your video file
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    # Some codecs report 0 FPS → fallback to None
    fps = fps if fps > 0 else None
    return frame_count, fps


# ----------------------------------------------------------------------
def get_info_ffprobe(video_path):
    """Return (frame_count, fps) using ffprobe, or (None, None) on error."""
    if not os.path.exists(video_path):
        return None, None

    try:
        # ffprobe command for frame count
        cmd_frames = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-count_frames', '-show_entries', 'stream=nb_read_frames',
            '-of', 'csv=p=0', video_path
        ]
        result_frames = subprocess.run(
            cmd_frames, capture_output=True, text=True, check=True
        )
        frame_count = int(result_frames.stdout.strip())

        # ffprobe command for FPS (r_frame_rate)
        cmd_fps = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=r_frame_rate',
            '-of', 'csv=p=0', video_path
        ]
        
        result_fps = subprocess.run(
            cmd_fps, capture_output=True, text=True, check=True
        )
        fps_str = result_fps.stdout.strip()
        if '/' in fps_str:
            num, den = map(int, fps_str.split('/'))
            fps = num / den if den != 0 else None
        else:
            fps = float(fps_str) if fps_str else None

        return frame_count, fps

    except subprocess.CalledProcessError:
        return None, None
    except FileNotFoundError:
        print("Error: ffprobe not found. Install ffmpeg.", file=sys.stderr)
        return None, None
    except Exception:
        return None, None


# ----------------------------------------------------------------------
def format_value(val):
    """Helper to show 'N/A' instead of None."""
    return f"{val:.6f}" if isinstance(val, float) else (val if val is not None else "N/A")



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

# ----------------------------------------------------------------------
BASE_PATH = Path("/Users/macbookair/Desktop/Video_RSL_UzSL/signer01")

def main():
    print("\n" + "=" * 80)
    print("  FRAME & FPS CHECK FOR ALL rep-*/video.mp4")
    print("=" * 80 + "\n")

    for word in top_100_words:
        video_dir = BASE_PATH / word / "videos"

        if not video_dir.is_dir():
            print(f"[MISSING] {word} → {video_dir}  (folder not found)")
            print()
            continue

        # Show what is inside the videos folder (optional, nice for debugging)
        print(f"\n{word}  ({video_dir})")
        print(f"   videos/ contents: {sorted(os.listdir(video_dir))}")

        found_any = False
        for rep_id in range(3):
            rep_dir = video_dir / f"rep-{rep_id}"
            mp4_path = rep_dir / "video.mp4"

            if not mp4_path.is_file():
                print(f"   rep-{rep_id}:  [MISSING] video.mp4")
                continue

            found_any = True
            cv2_frames, cv2_fps = get_info_cv2(str(mp4_path))
            ff_frames, ff_fps = get_info_ffprobe(str(mp4_path))

            # ---- pretty table for this repetition ----
            header = f"   rep-{rep_id}  →  {mp4_path.name}"
            print(header)
            print("   " + "-" * len(header))
            print(f"   {'Method':<10} {'Frames':<12} {'FPS':<12}")
            print(f"   {'cv2':<10} {format_value(cv2_frames):<12} {format_value(cv2_fps):<12}")
            print(f"   {'ffprobe':<10} {format_value(ff_frames):<12} {format_value(ff_fps):<12}")
            print()

        if not found_any:
            print("   [WARN] No rep-*/video.mp4 found for this word.\n")


if __name__ == "__main__":
    main()