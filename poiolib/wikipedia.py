import os
import sys
import subprocess
import urllib
import re
import glob
import shutil
import json
import tempfile

import requests
from bs4 import BeautifulSoup

from .langinfo import LangInfo

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def extract_to_txt(iso_639_3: str, output_filename: str):
    """
    Download and extract a Wikipedia to the given text file.

    Parameters
    ----------
    iso_639_3 : str
    	The ISO code of the Wikiepedia to download
    output_filename : str
    	The path to the text file to output the Wikipedia data. We will write
        one article per line.
    """
    tmp_dir = os.path.join(tempfile.gettempdir(), "poio-corpus-data", iso_639_3)
    extract_to(iso_639_3, tmp_dir)
    re_emptyspace = re.compile(r"[\t\n]+")
    re_wordbeg = re.compile(r"(?<=\s)[-']")
    re_wordend = re.compile(r"[-'](?=\s)")
    with open(output_filename, "w", encoding="utf-8") as output:
        for wiki_file in glob.glob(os.path.join(tmp_dir, "**", "wiki_*")):
            with open(wiki_file, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    article_data = json.loads(line)
                    article_text = article_data["text"]
                    article_text = re_emptyspace.sub(" ", article_text)
                    article_text = re_wordbeg.sub("", article_text)
                    article_text = re_wordend.sub("", article_text)
                    if len(article_text) > 200:
                        output.write(article_text)
                        output.write("\n")
    shutil.rmtree(tmp_dir)


def extract_to(iso_639_3: str, output_path: str):
    """
    Download and extract a Wikipedia to the given path.

    The download folder will be created if it does not exist.

    Parameters
    ----------
    iso_639_3 : str
    	The ISO code of the Wikiepedia to download
    output_path : str
    	The path to store the extracted data. We use Wikiextractor the the output
        will be organized in sub-directories, where each sub-directory contains a
        list of JSONL files.
    """
    langinfo = LangInfo()
    iso_639_1 = langinfo.iso_639_1_for_3(iso_639_3)
    if iso_639_1 == "":
        iso_639_1 = iso_639_3
    wiki_date, dump_link = get_dump_link(iso_639_1)
    in_wiki_prefix = iso_639_1 + "wiki"
    out_wiki_prefix = iso_639_3 + "wiki"
    file_path = download_dump(dump_link, output_path)
    wikipedia_extractor(file_path, output_path)


def _dump_link_from_lang_page(wiki_name: str, page: str) -> (str, str):
    """
    Get the link to the Wikipedia dump from the language page.

    Parameters
    ----------
    wiki_name : str
        The wiki name at Wikipedia of the language to get the link for, i.e.
        "dewiki".
    page : str
        The URL of the language page with the dump link.

    Returns
    -------
    (str, str)
        A tuple with the date of the Wikipedia dump and the link to the dump.
    """
    html_page = requests.get(page)
    soup = BeautifulSoup(html_page.content, features="html.parser")
    all_links = soup("a")
    for l in all_links:
        match = re.match(wiki_name + "-(\d{8})-pages-articles.xml.bz2", l.string)
        if match:
            wiki_date = match.group(1)
            dump_link = urllib.parse.urljoin(page, l["href"])
            return wiki_date, dump_link
    return None, None


def get_dump_link(iso_639_1: str) -> (str, str):
    """
    Get the dump link of the Wikipedia for the given ISO code.

    Parameters
    ----------
    iso_639_1 : str
        The ISO of the Wikipedia to get the dump link for.

    Returns
    -------
    (str, str)
        A tuple with the date of the Wikipedia dump and the link to the dump.
    """
    url = "https://dumps.wikimedia.org/backup-index.html"
    wiki_prefix = iso_639_1 + "wiki"
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, features="html.parser")

    page = None
    for link in soup("a"):
        if link.string == wiki_prefix:
            page = urllib.parse.urljoin(url, link["href"])

    # get the link for the dump file
    return _dump_link_from_lang_page(wiki_prefix, page)


def download_dump(dump_link: str, download_path: str) -> str:
    """
    Download a Wikipedia dump.

    The download folder will be created if it does not exist.

    Parameters
    ----------
    dump_link : str
        The link to the dump to download
    download_path : str
        A path where to store the downloaded file.

    Returns
    -------
    str
        The path the the downloaded dump file.
    """
    file_name = dump_link.split("/")[-1]
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    file_path = os.path.join(download_path, file_name)
    if not os.path.exists(file_path):
        r = requests.get(dump_link)
        with open(file_path, "wb") as f:
            f.write(r.content)
    return file_path


def wikipedia_extractor(file_path: str, output_path: str):
    """
    Extract Wikipedia data (articles) from a dump file.
    
    We use WikiExtractor to extract the data:
    https://github.com/attardi/wikiextractor

    Parameters
    ----------
    file_path : str
        The path to the dump file.
    output_path : str
        The output path for the extracted data. WikiExtractor will create
        sub-directories with JSONL files in each sub-directory.

    Returns
    -------
    (str, str)
        The standard output and error output of the WikiExtractor.
    """
    out = None
    err = None

    proc = subprocess.Popen(
        [
            sys.executable,
            os.path.join(SCRIPT_DIR, "WikiExtractor.py"),
            file_path,
            "--json",
            "-q",
            "-b",
            "100M",
            "-o",
            output_path,
        ],
        stdout=subprocess.PIPE,
    )
    (out, err) = proc.communicate()
    return (out, err)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Run: python -m poiolib.wikipedia iso_639_1 output_path")
        sys.exit()

    extract_to(sys.argv[1], sys.argv[2])
