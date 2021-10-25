import time
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Asset
from .utils import login_required


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    ctx = {"nav": "computer"}
    return render(request, "active_computer_assets.html", ctx)


@login_required()
def misc_asset_view(request: HttpRequest) -> HttpResponse:
    ctx = {"nav": "misc"}
    return render(request, "active_misc_assets.html", ctx)

@login_required()
def fobs_asset_view(request: HttpRequest) -> HttpResponse:
    ctx = {"nav": "fobs"}
    return render(request, "active_fobs_assets.html", ctx)


@login_required()
def disposed_asset_view(request: HttpRequest) -> HttpResponse:
    ctx = {"nav": "disposed"}
    return render(request, "disposed_assets.html", ctx)


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
        filter_arg = request.GET.get("filter")

        return JsonResponse({"items": Asset.search(filter_arg)})

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
