"""实验一的最小可运行程序：统计一段文本的字符数与行数。"""

import sys


def count(text: str) -> tuple[int, int]:
    return len(text), len(text.splitlines())


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            text = f.read()
    else:
        text = "hello git\nhello github\n"
    chars, lines = count(text)
    print(f"chars={chars} lines={lines}")


if __name__ == "__main__":
    main()
