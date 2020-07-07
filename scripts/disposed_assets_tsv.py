import datetime
import requests

# asset_register_url = "http://localhost:8000"
asset_register_url = "https://asset-register.tools.bink.sh"


def parse_date(value: str) -> str:
    if value:
        date = datetime.datetime.strptime(value, "%d-%b-%y")
        value = date.isoformat()

    return value


data = open("data/disposed_assets.tsv", "r").read().splitlines()
columns = (
    "id",
    "description",
    "hdd",
    "ram",
    "serial_number",
    "manufacturer",
    "asset_keeper",
    "disposal_date",
    "disposal_method",
    "disposal_sold_to",
    "disposal_sale_price",
    "disposal_finance_informed_date",
)

rows = []
for item in data:
    parts = [part.strip() for part in item.split("\t")]
    if len(parts) < len(columns):
        parts.extend([""] * (len(columns) - len(parts)))
    row = dict(zip(columns, parts))
    row["disposal_date"] = parse_date(row["disposal_date"])
    row["disposal_finance_informed_date"] = parse_date(row["disposal_finance_informed_date"])

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

    if row["disposal_sale_price"]:
        row["disposal_sale_price"] = float(row["disposal_sale_price"].replace(",", "").strip("£"))

    row["type"] = "LAPTOP"
    row["state"] = "DISPOSED"

    row["metadata"] = {"ram": row["ram"], "disk": row["hdd"]}
    row["disposal_finance_informed"] = True

    for key in ("ram", "hdd"):
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
