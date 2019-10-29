import unittest

import poiolib


class TestLangInfo(unittest.TestCase):
    def setUp(self):
        self.langinfo = poiolib.LangInfo()

    def test_iso_639_1_for_3(self):
        self.assertEqual(self.langinfo.iso_639_1_for_3("bar"), "")
        self.assertEqual(self.langinfo.iso_639_1_for_3("deu"), "de")
        with self.assertRaises(KeyError):
            self.langinfo.iso_639_1_for_3("not_existing")

    def test_iso_639_3_for_1(self):
        self.assertEqual(self.langinfo.iso_639_3_for_1("de"), "deu")
        self.assertEqual(self.langinfo.iso_639_3_for_1("bar"), "")


if __name__ == "__main__":
    unittest.main()
