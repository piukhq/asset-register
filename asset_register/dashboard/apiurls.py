from django.urls import path

from . import views

urlpatterns = [
    # /api/asset
    path("asset", views.ApiAssetView.as_view(), name="api_asset"),
    path("asset/<str:asset_id>", views.ApiAssetView.as_view(), name="api_asset_id"),
]
