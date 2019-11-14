import os
import unittest

import poiolib.ngrams

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestNgrams(unittest.TestCase):
    def test_corpus_ngrams(self):
        corpus_file = os.path.join(SCRIPT_DIR, "test_data", "der_linksdenker.txt")
        ngram_map = poiolib.ngrams.corpus_ngrams([corpus_file], 1)
        result = {tuple(ngram): count for ngram, count in ngram_map.items()}
        self.assertIn(("Der",), result)
        self.assertNotIn(("-über",), result)
        self.assertEqual(result[("Der",)], 12)
        self.assertEqual(result[("über",)], 3)
        ngram_map = poiolib.ngrams.corpus_ngrams([corpus_file], 2)
        result = {tuple(ngram): count for ngram, count in ngram_map.items()}
        self.assertIn(("Der", "Linksdenker"), result)
        self.assertEqual(result[("Der", "Linksdenker")], 2)
