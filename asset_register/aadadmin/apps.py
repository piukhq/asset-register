from django.contrib.admin.apps import AdminConfig


class AADAdminConfig(AdminConfig):
    default_site = "aadadmin.admin.AADAdminSite"
