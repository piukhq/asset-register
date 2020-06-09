import time
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Asset
from .utils import login_required


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "active_assets.html")


def test_delay(request: HttpRequest) -> HttpResponse:
    time.sleep(10)

    return JsonResponse({"status": "ok"})


@login_required()
def add_asset_view(request: HttpRequest) -> HttpResponse:
    ctx = {"types": Asset.ITEM_TYPE}
    return render(request, "add_asset.html", ctx)


@login_required()
def asset_view(request: HttpRequest, asset_id: str) -> HttpResponse:
    obj = get_object_or_404(Asset, id=asset_id)

    ctx = {"asset": obj}
    return render(request, "asset.html", ctx)


# /api/asset  TODO should use DRF
@method_decorator(login_required(api=True), name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class ApiAssetView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return JsonResponse({"items": Asset.search()})

    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            json_data = json.loads(request.body)
        except ValueError:
            return JsonResponse({"error": "invalid JSON data"}, status=400)

        asset_id = json_data["id"].strip()
        allow_overwrite = request.GET.get("allow_overwrite", "false") == "true"
        if asset_id == "":
            return JsonResponse({"error": "Asset ID cannot be empty"}, status=400)

        try:
            Asset.create(json_data, allow_overwrite=allow_overwrite)
        except Exception as err:
            return JsonResponse({"error": str(err)}, status=400)

        return JsonResponse({"url": reverse("asset_view", kwargs={"asset_id": asset_id})}, status=200)
