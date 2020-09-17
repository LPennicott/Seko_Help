import csv, os, xml.etree.ElementTree as ET

os.chdir(r"C:\Users\LChau\OneDrive\Seko Help\files")

filename = "90410242013_EXCEL_ON_FILE_HAWBS.csv"

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    hawbs = {str(row["Hawb"]) for row in reader}

xmlfile = "904-10242013.xml"

with open(xmlfile, "rb") as xfile:
    parsed_xml = ET.parse(xfile)

parsed_xml_root = parsed_xml.getroot()

parsed_list = parsed_xml_root.findall("ENTRY")

for item in parsed_list:
    if item.find("MANIFEST").find("HOUSE").text not in hawbs:
        parsed_xml_root.remove(item)

parsed_xml.write("new_file.xml", xml_declaration=True)
