# Generated by Django 3.0.7 on 2020-07-07 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0005_auto_20200707_1126"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="asset_keeper",
            field=models.CharField(max_length=128, null=True),
        ),
    ]
