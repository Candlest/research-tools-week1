"""运行方法：python3 -m unittest discover -s code -p 'test_*.py' -v。"""

import csv
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from text_stats import word_frequencies


class WordFrequencyTests(unittest.TestCase):
    def test_lowercase_and_nonletter_separators(self):
        self.assertEqual(
            word_frequencies("HELLO, hello! World123world_test\nTEST."),
            [("hello", 2), ("world", 2), ("test", 2)],
        )

    def test_empty_tokens_are_filtered(self):
        for text in ("", " 123...\n中文 "):
            with self.subTest(text=text):
                self.assertEqual(word_frequencies(text), [])

    def test_descending_frequency_and_top_limit(self):
        self.assertEqual(
            word_frequencies("rare common middle common middle common", top=2),
            [("common", 3), ("middle", 2)],
        )

    def test_cli_default_and_custom_top_with_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "code").mkdir()
            script = root / "code" / "text_stats.py"
            shutil.copyfile(Path(__file__).with_name("text_stats.py"), script)
            source = root / "input.txt"
            words = "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda".split()
            source.write_text(" ".join(words), encoding="utf-8")
            for options, limit in (([], 10), (["--top", "3"], 3)):
                with self.subTest(options=options):
                    result = subprocess.run(
                        [sys.executable, str(script), str(source), *options],
                        cwd=root, capture_output=True, text=True, check=True,
                    )
                    self.assertEqual(
                        result.stdout.splitlines(),
                        [f"{word}\t1" for word in words[:limit]],
                    )
                    with (root / "result" / "word_freq.csv").open(
                        encoding="utf-8", newline=""
                    ) as file:
                        self.assertEqual(
                            list(csv.reader(file)),
                            [["word", "count"]] + [[word, "1"] for word in words[:limit]],
                        )


if __name__ == "__main__":
    unittest.main()
