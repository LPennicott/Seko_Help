import csv
import os
import datetime
import sys
from . import gui.gui_tools


def csv_collection():

    folder = gui.gui_tools._standard_get_folder()
    files = os.listdir(folder)
    csv_files = [file for file in files if file.endswith(".csv")]

    new_csv_file_content = []
    for item in csv_files:
        mawb = {"mawb": item.split(".")[0]}
        with open(item, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, dialect="excel")

            for row in reader:
                row = {**mawb, **row}
                new_csv_file_content.append(row)

    return new_csv_file_content


def new_csv_file(csv_content):

    fieldnames = [
        "mawb",
        "consignor_item_id",
        "display_id",
        "receptacle_id",
        "tracking_number",
        "sender_name",
        "sender_orgname",
        "sender_address1",
        "sender_address2",
        "sender_district",
        "sender_city",
        "sender_state",
        "sender_zip5",
        "sender_zip4",
        "sender_country",
        "sender_phone",
        "sender_email",
        "sender_url",
        "recipient_name",
        "recipient_orgname",
        "recipient_address1",
        "recipient_address2",
        "recipient_district",
        "recipient_city",
        "recipient_state",
        "recipient_zip5",
        "recipient_zip4",
        "recipient_country",
        "recipient_phone",
        "recipient_email",
        "recipient_addr_type",
        "return_name",
        "return_orgname",
        "return_address1",
        "return_address2",
        "return_district",
        "return_city",
        "return_state",
        "return_zip5",
        "return_zip4",
        "return_country",
        "return_phone",
        "return_email",
        "mail_type",
        "pieces",
        "weight",
        "length",
        "width",
        "height",
        "girth",
        "value",
        "machinable",
        "po_box_flag",
        "gift_flag",
        "commercial_flag",
        "customs_quantity_units",
        "dutiable",
        "duty_pay_by",
        "product",
        "description",
        "url",
        "sku",
        "country_of_origin",
        "manufacturer",
        "Harmonization_code",
        "unit_value",
        "quantity",
        "total_value",
        "total_weight",
    ]

    with open(f"{datetime.date.today()}", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_content:
            writer.writerow(row)

    return


if __name__ == "__main__":
    item = csv_collection(
        r"C:\Users\LChau\OneDrive\Data Analysis Projects\Seko\morningg"
    )

    new_csv_file(item)
