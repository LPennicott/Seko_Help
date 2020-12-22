# -*- coding: utf-8 -*-
import csv
import xml.etree.ElementTree as ET
import collections
import itertools


def _isEnglish(text):
    try:
        text.encode(encoding="utf-8").decode("ascii")
    except UnicodeDecodeError:
        return False
    else:
        return True


def test_house_bills_hs_codes(xmlfile):

    with open(xmlfile, "rb") as xfile:
        parsed_xml = ET.parse(xfile)

    parsed_xml_root = parsed_xml.getroot()
    entries_list = parsed_xml_root.findall("ENTRY")

    bad_hawb = set()
    for elem in parsed_xml.iter("ENTRY"):
        for item in elem.iter("CARGO_RELEASE_ITEM"):
            if item.find("HTS").text == "#N/A":
                bad_hawb.add(elem.find("MANIFEST").find("HOUSE").text)

    for entry in entries_list:
        if entry.find("MANIFEST").find("HOUSE").text in bad_hawb:
            parsed_xml_root.remove(entry)

    return bad_hawb, entries_list, parsed_xml


def collect_hawb_and_hs_codes(csvfile):

    with open(csvfile, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, dialect="excel")
        hawbs_hs = [
            (item["consignor_item_id"], item["Harmonization_code"])
            for item in reader
        ]
        hawbs = {
            hawb: [i[1] for i in e]
            for hawb, e in itertools.groupby(hawbs_hs, lambda x: x[0])
        }
    return hawbs


def fix_xml_file(xmlfile, csvfile):

    bad_hawbs = test_house_bills_hs_codes(xmlfile)[0]
    entries = test_house_bills_hs_codes(xmlfile)[1]
    new_xml = test_house_bills_hs_codes(xmlfile)[2]
    hawb_hs_codes = collect_hawb_and_hs_codes(csvfile)

    for item in entries:
        if item.find("MANIFEST").find("HOUSE").text in bad_hawbs:
            hs_codes = hawb_hs_codes.get(
                item.find("MANIFEST").find("HOUSE").text
            )
            for parcel, hs in zip(
                item.findall("CARGO_RELEASE_ITEM"), hs_codes
            ):
                print(item.find("MANIFEST").find("HOUSE").text, hs)
                parcel.find("HTS").text = hs
            new_xml.getroot().append(item)

    new_xml.write("784-13165946_fixed.xml", xml_declaration=True)


if __name__ == "__main__":
    # check, double_check = test_house_bills_hs_codes("784-13165946_SFO.xml")
    # print(len(check), check)
    # print(len(double_check), double_check)
    # print(collections.Counter(double_check).most_common(1)[0][0])

    # hs = collect_hawb_and_hs_codes("784-13165946 (4451).csv")
    # print(len(hs), hs)

    fix_xml_file("784-13165946_SFO.xml", "784-13165946 (4451).csv")
