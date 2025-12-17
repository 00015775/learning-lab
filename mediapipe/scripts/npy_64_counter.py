# check_npy_counts.py
from pathlib import Path
from collections import defaultdict

# ------------------------------------------------------------------
# CONFIG – change only if your path is different
# ------------------------------------------------------------------
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

REQUIRED_NPY_PER_REP = 64

# ------------------------------------------------------------------
# MAIN CHECK
# ------------------------------------------------------------------
def main():
    problems = []
    total_signs = len(top_100_words)
    ok_count = 0

    print(f"Checking {total_signs} signs for exactly {REQUIRED_NPY_PER_REP} .npy files per rep...\n")

    for word in top_100_words:
        lm_base = BASE_PATH / word / "landmarks"
        if not lm_base.exists():
            problems.append(f"{word} → landmarks folder missing")
            continue

        sign_ok = True
        rep_issues = []

        for rep_dir in lm_base.iterdir():
            if not rep_dir.is_dir() or not rep_dir.name.startswith("rep-"):
                continue

            npy_files = list(rep_dir.glob("*.npy"))
            count = len(npy_files)

            if count != REQUIRED_NPY_PER_REP:
                sign_ok = False
                rep_issues.append(f"  • {rep_dir.name}: {count} (expected {REQUIRED_NPY_PER_REP})")

        if not sign_ok:
            problems.append(f"{word}:\n" + "\n".join(rep_issues))
        else:
            ok_count += 1

    # ------------------- PRINT RESULTS -------------------
    if problems:
        print("PROBLEMATIC SIGNS (not 64 .npy files):")
        print("-" * 50)
        for p in problems:
            print(p)
        print("-" * 50)
    else:
        print("ALL SIGNS ARE PERFECT! Every rep has exactly 64 .npy files.")

    print(f"\nSummary: {ok_count}/{total_signs} signs are correct.")
    if ok_count < total_signs:
        print(f"   → {total_signs - ok_count} signs need fixing.")

if __name__ == "__main__":
    main()