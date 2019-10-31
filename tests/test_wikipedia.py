import unittest
import os
import shutil
import tempfile
import glob

import poiolib.wikipedia


class TestWikipedia(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = os.path.join(tempfile.gettempdir(), "poio-test-data")
        os.makedirs(self.tmp_dir)

    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def test_extract_to_text(self):
        output_file = os.path.join(self.tmp_dir, "cre.txt")
        poiolib.wikipedia.extract_to_txt("cre", output_file)
        self.assertTrue(os.path.isfile(output_file))
        self.assertNotEqual(os.path.getsize(output_file), 0)

    def test_extract_to(self):
        poiolib.wikipedia.extract_to("cre", self.tmp_dir)
        self.assertEqual(
            len(glob.glob(os.path.join(self.tmp_dir, "crwiki*.xml.bz2"))), 1
        )
        self.assertTrue(os.path.isfile(os.path.join(self.tmp_dir, "AA", "wiki_00")))

    def test_get_dump_link(self):
        (date, link) = poiolib.wikipedia.get_dump_link("cr")
        self.assertIn("crwiki", link)
        self.assertIn("pages-articles.xml.bz2", link)

    def test_download_dump(self):
        (date, dumplink) = poiolib.wikipedia.get_dump_link("cr")
        filepath = poiolib.wikipedia.download_dump(dumplink, self.tmp_dir)
        self.assertTrue(os.path.isfile(os.path.join(filepath)))
        self.assertEqual(
            len(glob.glob(os.path.join(self.tmp_dir, "crwiki*.xml.bz2"))), 1
        )

    def test_wikipedia_extractor(self):
        (date, dumplink) = poiolib.wikipedia.get_dump_link("cr")
        filepath = poiolib.wikipedia.download_dump(dumplink, self.tmp_dir)
        poiolib.wikipedia.wikipedia_extractor(filepath, self.tmp_dir)
        self.assertTrue(os.path.isfile(os.path.join(self.tmp_dir, "AA", "wiki_00")))
