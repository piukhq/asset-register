from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    path("misc", views.misc_asset_view, name="misc_assets"),
    path("azure", views.azure_asset_view, name="azure_assets"),
    path("disposed", views.disposed_asset_view, name="disposed_assets"),
    path("add_asset", views.add_asset_view, name="add_asset"),
    path("test_delay", views.test_delay, name="test_delay"),
    path("asset/<str:asset_id>", views.asset_view, name="asset_view"),
]
