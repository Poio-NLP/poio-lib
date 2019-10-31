import unittest
from collections.abc import Iterable

import poiolib


class TestLangInfo(unittest.TestCase):
    def setUp(self):
        self.langinfo = poiolib.LangInfo()

    def test_languages(self):
        languages = self.langinfo.languages()
        self.assertIsInstance(languages, Iterable)
        self.assertNotEqual(len(languages), 0)

    def test_iso_639_1_for_3(self):
        self.assertEqual(self.langinfo.iso_639_1_for_3("bar"), "")
        self.assertEqual(self.langinfo.iso_639_1_for_3("deu"), "de")
        with self.assertRaises(KeyError):
            self.langinfo.iso_639_1_for_3("not_existing")

    def test_iso_639_3_for_1(self):
        self.assertEqual(self.langinfo.iso_639_3_for_1("de"), "deu")
        self.assertEqual(self.langinfo.iso_639_3_for_1("bar"), "")

    def test_langname_for_iso(self):
        self.assertEqual(self.langinfo.langname_for_iso("deu"), "German")
        self.assertEqual(self.langinfo.langname_for_iso("bar"), "Bavarian")


if __name__ == "__main__":
    unittest.main()
