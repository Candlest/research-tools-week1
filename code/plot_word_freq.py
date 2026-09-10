"""读取 result/word_freq.csv，导出矢量柱状图 figures/word_freq.pdf。"""

import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "result" / "word_freq.csv"
OUT = ROOT / "figures" / "word_freq.pdf"

matplotlib.rcParams.update({
    "pdf.fonttype": 42,
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def main() -> None:
    with CSV.open(encoding="utf-8") as f:
        rows = [(r["word"], int(r["count"])) for r in csv.DictReader(f)]
    rows = rows[:10][::-1]
    words = [w for w, _ in rows]
    counts = [c for _, c in rows]

    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    bars = ax.barh(words, counts, color="#3f6fb5", height=0.65)
    ax.bar_label(bars, padding=3, fontsize=8, color="#333333")
    ax.set_xlabel("occurrences")
    ax.set_xlim(0, max(counts) * 1.18)
    ax.grid(axis="x", color="#dddddd", linewidth=0.6)
    ax.set_axisbelow(True)
    OUT.parent.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
