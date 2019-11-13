import os
import unittest

import poiolib.corpus


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class TestCorpusReader(unittest.TestCase):
    def setUp(self):
        self.corpus_reader = poiolib.corpus.CorpusReader(
            os.path.join(SCRIPT_DIR, "test_data")
        )

    def test_documents(self):
        document = next(self.corpus_reader.documents())
        self.assertEqual(len(document), 33)

    def test_sentences(self):
        sentence = next(self.corpus_reader.sentences())
        self.assertEqual(len(sentence), 33)

    def test_tokenized_sentences(self):
        tokens = next(self.corpus_reader.tokenized_sentences())
        self.assertEqual(next(tokens), "Der")
        self.assertEqual(next(tokens), "Linksdenker")
