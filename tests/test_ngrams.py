import os
import unittest

import poiolib.ngrams

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestNgrams(unittest.TestCase):
    def test_corpus_ngrams(self):
        corpus_file = os.path.join(SCRIPT_DIR, "test_data", "der_linksdenker.txt")
        ngram_map = poiolib.ngrams.corpus_ngrams([corpus_file], 1)
        (ngram, count) = next(ngram_map.items())
        self.assertEqual(ngram, ["Der"])
        self.assertEqual(count, 12)
        ngram_map = poiolib.ngrams.corpus_ngrams([corpus_file], 2)
        (ngram, count) = next(ngram_map.items())
        self.assertEqual(ngram, ["Der", "Linksdenker"])
        self.assertEqual(count, 2)
