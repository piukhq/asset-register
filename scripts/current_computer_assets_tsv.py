import datetime

import requests

# asset_register_url = "http://localhost:8000"
asset_register_url = "https://asset-register.tools.bink.sh"


def parse_date(value: str) -> str:
    if value:
        date = datetime.datetime.strptime(value, "%d-%b-%y")
        value = date.isoformat()

    return value


data = open("data/current_computer_asset.tsv", "r").read().splitlines()
columns = (
    "id",
    "description",
    "hdd",
    "ram",
    "serial_number",
    "manufacturer",
    "cost",
    "vat",
    "total_cost",
    "asset_keeper",
    "purchase_date",
    "warranty_date",
)

rows = []
for item in data:
    parts = [part.strip() for part in item.split("\t")]
    if len(parts) < len(columns):
        parts.extend([""] * (len(columns) - len(parts)))
    row = dict(zip(columns, parts))
    row["purchase_date"] = parse_date(row["purchase_date"])
    row["warranty_date"] = parse_date(row["warranty_date"])

    for col in columns:
        if not row[col]:
            row[col] = None

    if row["hdd"]:
        if "TB" in row["hdd"]:
            row["hdd"] = int(row["hdd"].replace("TB", "")) * 1024
        else:
            row["hdd"] = int(row["hdd"].replace("GB", ""))
    if row["ram"]:
        row["ram"] = int(row["ram"].replace("GB", ""))

    if row["cost"]:
        row["cost"] = float(row["cost"].replace(",", "").strip("£"))
    if row["vat"]:
        row["vat"] = float(row["vat"].replace(",", "").strip("£"))

    row["type"] = "LAPTOP"

    row["metadata"] = {"ram": row["ram"], "disk": row["hdd"]}

    for key in ("total_cost", "ram", "hdd"):
        del row[key]

    # if row['id'] != 'MAC127':
    #     continue

    resp = requests.post(
        f"{asset_register_url}/api/asset?allow_overwrite=true",
        json=row,
        headers={"Authorization": "Token 7bb4810d-6af0-484d-9595-3402c75bfdc3"},
    )
    if resp.status_code != 200:
        print(resp.text)
    print(f'Posted {row["id"]}')
    rows.append(row)

print()
