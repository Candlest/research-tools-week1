"""统计英文词频，在终端和 CSV 中输出前 N 个词。"""

import argparse
from collections import Counter
import csv
from pathlib import Path
import re


def word_frequencies(text: str, top: int = 10) -> list[tuple[str, int]]:
    words = (word for word in re.split(r"[^a-z]+", text.lower()) if word)
    return Counter(words).most_common(top)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="UTF-8 文本文件路径")
    parser.add_argument("--top", type=int, default=10, help="输出词数，默认 10")
    args = parser.parse_args()
    if args.top < 1:
        parser.error("--top 必须为正整数")

    rows = word_frequencies(args.file.read_text(encoding="utf-8"), args.top)
    output = Path(__file__).resolve().parent.parent / "result" / "word_freq.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["word", "count"])
        writer.writerows(rows)
    for word, count in rows:
        print(f"{word}\t{count}")


if __name__ == "__main__":
    main()
