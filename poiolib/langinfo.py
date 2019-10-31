import os
import csv
import json

from typing import List

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


class LangInfo:
    """
    This class provides info about language codes and names. It contains some
    helper methods to map between names and codes.
    """

    def __init__(self):
        self.init_iso_map()

    def init_iso_map(self):
        langinfo_file = os.path.join(SCRIPT_DIR, "data", "langinfo.json")
        with open(langinfo_file, "r", encoding="utf-8") as f:
            self.iso_info_map = json.load(f)

    def languages(self) -> List[str]:
        """
        Get a list of supported languages, as ISO 639-3 codes.

        Returns
        -------
        array of str
            An array of ISO 639-3 codes.
        """
        return self.iso_info_map.keys()

    def iso_639_1_for_3(self, iso_639_3: str) -> str:
        """
        Return an ISO 639-1 code for a given ISO 639-3 code.

        Parameters
        ----------
        iso_639_3 : str
            The ISO 639-3 code to look up

        Returns
        -------
        str
            The ISO 639-1 code for the given code. Returns an empty string if
            there is no ISO 639-1 code for the given code.
        """
        return self.iso_info_map[iso_639_3]["iso_639_1"]

    def iso_639_3_for_1(self, iso_639_1: str) -> str:
        """
        Return an ISO 639-3 code for a given ISO 639-1 code.

        Parameters
        ----------
        iso_639_1 : str
            The ISO 639-1 code to look up.

        Returns
        -------
        str
            The ISO 639-3 code for the given code. Returns an empty string if
            there is no ISO 639-3 code for the given code.
        """
        iso_639_1_map = {
            values["iso_639_1"]: iso_639_3
            for iso_639_3, values in self.iso_info_map.items()
            if values["iso_639_1"] != ""
        }
        return iso_639_1_map.get(iso_639_1, "")

    def langname_for_iso(self, iso_639_3: str):
        """
        Return language name for a given ISO 639-3 code.

        Parameters
        ----------
        iso_639_3 : str
            The ISO 639-3 code to look up

        Returns
        -------
        str
            The language name for the given code.
        """
        return self.iso_info_map[iso_639_3]["language_name"]

    def geoinfo_for_iso(self, iso_639_3: str):
        """
        Return geo information for a given ISO 639-3 code.

        Parameters
        ----------
        iso_639_3 : str
            The ISO 639-3 code to look up.

        Returns
        -------
        dict
            The geo information for the given code. The result dict has two
            keys, `long` and `lat`. Returns `None` if the language does not
            have geo information.
        """
        return self.iso_info_map[iso_639_3].get("geo", None)
