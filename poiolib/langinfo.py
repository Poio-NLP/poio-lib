import os
import csv

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


class LangInfo:
    """
    This class provides info about language codes and names. It contains some
    helper methods to map between names and codes.
    """

    def __init__(self):
        self.init_iso_map()

    def init_iso_map(self):
        iso_info_file = os.path.join(SCRIPT_DIR, "data", "iso-639-3.tab")
        self.iso_info_map = {}
        with open(iso_info_file, "r", encoding="utf-8") as f:
            iso_info_rows = csv.reader(f, delimiter="\t")
            next(iso_info_rows)
            for row in iso_info_rows:
                self.iso_info_map[row[0]] = {
                    "iso_639_1": row[3],
                    "language_name": row[6],
                }

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

    def langname_for_iso(self, iso_639_3):
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
