# Generated by Django 3.0.7 on 2020-07-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0004_auto_20200707_1110"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="cost",
            field=models.DecimalField(decimal_places=4, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name="asset",
            name="vat",
            field=models.DecimalField(decimal_places=4, max_digits=12, null=True),
        ),
    ]
