import datetime

import requests

# asset_register_url = "http://localhost:8000"
asset_register_url = "https://asset-register.tools.bink.sh"


def parse_date(value: str) -> str:
    if value:
        date = datetime.datetime.strptime(value, "%d-%b-%y")
        value = date.isoformat()

    return value


data = [
    ["MISC001", "Siobhan Goodman", "Apple", "Keyboard"],
    ["MISC002", "Hannah Soye", "Apple", "Magic Mouse"],
    ["MISC003", "Melanie Dibley", "Unknown", "Headset"],
    ["MISC004", "Amanda Hoy", "Logitech", "Mouse"],
    ["MISC005", "Amanda Hoy", "Apple", "Keyboard"],
    ["MISC006", "Iain Simmons", "Unknown", "Headset"],
    ["MISC007", "Ben Dillon", "Apple", "Magic Mouse"],
    ["MISC008", "Karine Pillet", "Apple", "Magic Mouse"],
    ["MISC009", "Nicki Fitzgerald", "Apple", "Magic Mouse"],
    ["MISC010", "Kirsten Harris", "Apple", "Magic Mouse"],
    ["MISC011", "Richard Evetts", "Apple", "Magic Mouse"],
    ["MISC012", "Ben Dillon", "Apple", "Keyboard"],
    ["MISC013", "Karine Pillet", "Apple", "Keyboard"],
    ["MISC014", "Nicki Fitzgerald", "Apple", "Keyboard"],
    ["MISC015", "Kirsten Harris", "Apple", "Keyboard"],
    ["MISC016", "Richard Evetts", "Apple", "Keyboard"],
]

columns = ("id", "asset_keeper", "manufacturer", "description")

rows = []
for item in data:
    parts = item
    if len(parts) < len(columns):
        parts.extend([""] * (len(columns) - len(parts)))
    row = dict(zip(columns, parts))

    row["type"] = "OTHER"

    # if row['id'] != 'MAC127':
    #     continue
    #
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
