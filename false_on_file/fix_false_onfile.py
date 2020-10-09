import csv
import os
import re
import logging
import xml.etree.ElementTree as ET


def process_files(csvfile, xmlfile, save_location):
    logging.basicConfig(
        filename=f'{save_location}{os.sep}{xmlfile.split("/")[-1].split()[0]}.log',
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(message)s"
    )

    # Open csvfile for list of HAWB Entries that need to be extracted from the xml file
    with open(csvfile, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, dialect='excel')

        # ensure that as long as there is a field that contains hawbs
        # it is found and selected to iterate through
        try:
            for fieldname in reader.fieldnames:
                if result := re.match('hawb', fieldname, re.IGNORECASE):
                    name = result.group(0)

        # collect hawbs to compare against hawb nodes in xml file
            hawbs = {str(row[name]) for row in reader}
        except:
            logging.error("Exception Occurred: ", exc_info=True)
        logging.debug(f'{len(hawbs)}')

        # New list to ensure all hawbs in list has length 11.
        new_hawbs = []
        for hawb in hawbs:
            while len(hawb) < 11:
                hawb = '0' + hawb
            new_hawbs.append(hawb)

        logging.debug(f'{new_hawbs}')

    with open(xmlfile, "rb") as xfile:
        parsed_xml = ET.parse(xfile)

    parsed_xml_root = parsed_xml.getroot()
    parsed_list = parsed_xml_root.findall("ENTRY")

    # if the Entry Element does not contain a HAWB in the csv file,
    # remove the entire Entry Element from the file.
    for item in parsed_list:
        if item.find("MANIFEST").find("HOUSE").text not in new_hawbs:
            parsed_xml_root.remove(item)

    csvname = csvfile.split('/')[-1].split()[0]

    parsed_xml.write(f"{save_location}{os.sep}{csvname}.xml", xml_declaration=True)
    return


if __name__ == '__main__':
    process_files('29736634846_ON_FILE_HAWBS_1.CSV', '297-36634846.xml', r'D:\GitHub\Seko_Help\\')
