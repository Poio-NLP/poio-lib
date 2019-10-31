import json
import re
import csv

import requests

re_lat = re.compile(r"<geo:lat[^>]*>([^<]*)</geo:lat>")
re_long = re.compile(r"<geo:long[^>]*>([^<]*)</geo:long>")


def long_lat_for_content(content):
    lat = None
    lng = None
    match_lat = re_lat.search(content)
    if match_lat:
        lat = match_lat.group(1)
    match_long = re_long.search(content)
    if match_long:
        lng = match_long.group(1)
    return (lng, lat)


def build_iso_map():
    iso_info_file = "iso-639-3.tab"
    iso_info_map = {}
    with open(iso_info_file, "r", encoding="utf-8") as f:
        iso_info_rows = csv.reader(f, delimiter="\t")
        next(iso_info_rows)
        for row in iso_info_rows:
            iso_info_map[row[0]] = {
                "iso_639_1": row[3],
                "language_name": row[6],
            }
    return iso_info_map


def main():
    iso_map = build_iso_map()
    for iso_639_3 in iso_map.keys():
        result = requests.get(
            "http://glottolog.org/resource/languoid/iso/{0}.rdf".format(iso_639_3)
        )
        try:
            result.raise_for_status()
            (lng, lat) = long_lat_for_content(result.content.decode("utf-8"))
        except requests.exceptions.HTTPError:
            lat = None
            lng = None
        if lng is not None and lat is not None:
            iso_map[iso_639_3]["geo"] = {"lat": lat, "long": lng}
        else:
            print("No geo info found for lang {}".format(iso_639_3))

    with open("langinfo.json", "w", encoding="utf-8") as f:
        json.dump(iso_map, f, indent=2)


if __name__ == "__main__":
    main()
