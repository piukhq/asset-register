from django.db import models
from django.contrib.postgres.fields import JSONField
from typing import Dict, Any, List
from django.urls import reverse
from django.utils.safestring import SafeString


class Asset(models.Model):
    STATES = (("ACTIVE", "Active"), ("DISPOSED", "Disposed"))

    ITEM_TYPE = (("MONITOR", "Monitor"), ("TV", "TV"), ("LAPTOP", "Laptop"), ("PHONE", "Phone"), ("OTHER", "Other"))

    id = models.CharField(max_length=10, primary_key=True)

    description = models.TextField(null=True)
    serial_number = models.CharField(max_length=64, null=True)
    manufacturer = models.CharField(max_length=32, null=True)
    metadata = JSONField(null=True)
    type = models.CharField(choices=ITEM_TYPE, max_length=16, null=False)

    state = models.TextField(choices=STATES, null=False, default="ACTIVE", max_length=16)

    # Misc
    cost = models.DecimalField(null=True, max_digits=7, decimal_places=4)
    vat = models.DecimalField(null=True, max_digits=7, decimal_places=4)
    asset_keeper = models.CharField(max_length=32, null=True)
    assigned_date = models.DateTimeField(null=True)

    disposal_date = models.DateTimeField(null=True, blank=True)
    disposal_method = models.CharField(max_length=32, null=True, blank=True)
    disposal_sale_price = models.DecimalField(null=True, max_digits=7, decimal_places=4, blank=True)

    def __repr__(self) -> str:
        return f"<Asset {str(self)}>"

    def __str__(self) -> str:
        return f"{self.id} ({self.type})"

    @classmethod
    def create(cls, data: Dict[str, Any]) -> None:
        # Shouldn't really do this but am lazy
        asset_id = data["id"]
        if cls.objects.filter(id=asset_id):
            raise Exception(f"Asset with id {asset_id} already exists")

        record = cls(**data)
        record.save()

    @classmethod
    def search(cls) -> List[Dict[str, Any]]:
        result = []

        for obj in cls.objects.all():
            result.append(
                {
                    "id": obj.id,
                    "type": obj.get_type_display(),
                    "owner": obj.asset_keeper,
                    "metadata": obj.string_metadata,
                    "view_url": reverse("asset_view", kwargs={"asset_id": obj.id}),
                    "api_url": reverse("api_asset_id", kwargs={"asset_id": obj.id}),
                }
            )

        return result

    @property
    def string_metadata(self) -> str:
        result = ""
        if self.type == "LAPTOP":
            result += self.manufacturer
            if model := self.metadata.get("model"):
                result += f" {model}"
            if ram := self.metadata.get("ram"):
                result += f" {ram}GB RAM"
            if ram := self.metadata.get("disk"):
                result += f" {ram}GB Disk"

        return result.strip()

    @property
    def html_metadata(self) -> SafeString:
        data = ""
        for key, value in self.metadata.items():
            data += f"{key}: {value}\n"

        result = f"<pre>{data.strip()}</pre>"
        return SafeString(result)

    @property
    def total_cost(self) -> float:
        result = 0.0
        if self.cost:
            result += float(self.cost)
        if self.vat:
            result += float(self.vat)
        return result
