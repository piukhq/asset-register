# Generated by Django 3.0.7 on 2020-07-07 11:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0003_auto_20200707_1059"),
    ]

    operations = [
        migrations.RenameField(
            model_name="asset",
            old_name="warrenty_date",
            new_name="warranty_date",
        ),
    ]
