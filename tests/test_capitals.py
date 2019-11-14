import os
import unittest

import poiolib.capitals

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCapitals(unittest.TestCase):
    def test_sentence_starts_capital_map(self):
        corpus_file = os.path.join(SCRIPT_DIR, "test_data", "der_linksdenker.txt")
        lower_map = poiolib.capitals.sentence_starts_capital_map([corpus_file])
        self.assertEqual(lower_map["Der"], "der")
