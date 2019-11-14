import os
import unittest

import poiolib.corpus


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class TestCorpusReader(unittest.TestCase):
    def setUp(self):
        self.documents = poiolib.corpus.corpus_documents(
            [os.path.join(SCRIPT_DIR, "test_data", "der_linksdenker.txt")]
        )

    def test_documents(self):
        document = next(self.documents)
        self.assertEqual(len(document), 33)

    def test_sentences(self):
        sentence = next(poiolib.corpus.sentences(next(self.documents)))
        self.assertEqual(len(sentence), 33)

    def test_tokenized_sentences(self):
        tokens = next(poiolib.corpus.tokenized_sentences(next(self.documents)))
        self.assertEqual(next(tokens), "Der")
        self.assertEqual(next(tokens), "Linksdenker")
