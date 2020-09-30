import csv
import os
import xml.etree.ElementTree as ET


csvlist = [csvfile for csvfile in os.listdir() if csvfile.endswith('.csv')]
xmllist = [xmlfile for xmlfile in os.listdir() if xmlfile.endswith('.xml')]

# Open csvfile for list of HAWB Entries that need to be extracted from the xml file
for csvfile, xmlfile in zip(csvlist, xmllist):
    with open(csvfile, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, dialect='excel')
        hawbs = {str(row["HAWB"]) for row in reader}

        # New list to ensure all hawbs in list has length 11.
        new_hawbs = []
        for hawb in hawbs:
            while len(hawb) < 11:
                hawb = '0' + hawb
            new_hawbs.append(hawb)

    with open(xmlfile, "rb") as xfile:
        parsed_xml = ET.parse(xfile)

    parsed_xml_root = parsed_xml.getroot()
    parsed_list = parsed_xml_root.findall("ENTRY")

    # if the Entry Element does not contain a HAWB in the csv file,
    # remove the entire Entry Element from the file.
    for item in parsed_list:
        if item.find("MANIFEST").find("HOUSE").text not in new_hawbs:
            parsed_xml_root.remove(item)

    parsed_xml.write(f"new_file {csvfile.split('.')[0]}.xml", xml_declaration=True)
