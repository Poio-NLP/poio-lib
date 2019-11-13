import os
import unittest

import poiolib.capitals

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCapitals(unittest.TestCase):
    def test_sentence_starts_lower_map(self):
        corpus_path = os.path.join(SCRIPT_DIR, "test_data")
        lower_map = poiolib.capitals.sentence_starts_lower_map(corpus_path)
        self.assertEqual(lower_map["Der"], "der")
