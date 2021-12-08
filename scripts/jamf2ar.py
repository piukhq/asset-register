import os

import requests

# asset_register_url = 'http://localhost:8000'
asset_register_url = "https://asset-register.tools.bink.sh"

jamf_auth = (os.getenv("JAMF_USER"), os.getenv("JAMF_PASSWORD"))

list_computers_resp = requests.get(
    "https://bink.jamfcloud.com/JSSResource/computers", auth=jamf_auth, headers={"Accept": "application/json"}
)
computers = list_computers_resp.json()["computers"]

for computer in computers:
    url = f'https://bink.jamfcloud.com/JSSResource/computers/id/{computer["id"]}'
    computer_resp = requests.get(url, auth=jamf_auth, headers={"Accept": "application/json"})
    data = computer_resp.json()["computer"]

    payload = {
        "id": "JAMF{0:04}".format(data["general"]["id"]),
        "description": "Imported from JAMF " + data["general"]["name"],
        "serial_number": data["general"]["serial_number"],
        "manufacturer": data["hardware"]["make"],
        "type": "LAPTOP",
        "metadata": {
            "model": data["hardware"]["model"],
            "ram": int(round(data["hardware"]["total_ram"] / 1024, 0)),
            "disk": int(round(data["hardware"]["storage"][0]["size"] / 1024, 0)),
            "os_version": data["hardware"]["os_version"],
            "processor_type": data["hardware"]["processor_type"],
        },
    }

    requests.post(
        f"{asset_register_url}/api/asset?allow_overwrite=true",
        json=payload,
        headers={"Authorization": "Token 7bb4810d-6af0-484d-9595-3402c75bfdc3"},
    )
    print(f'Posted {payload["id"]}')
