# Generated by Django 4.2.1 on 2023-06-12 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loginpage", "0003_amazonproduct_delete_product"),
    ]

    operations = [
        migrations.CreateModel(
            name="eBayProduct",
            fields=[
                ("product_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("price", models.CharField(max_length=50)),
                ("rating", models.CharField(max_length=10)),
                ("reviews", models.CharField(max_length=50)),
                ("availability", models.CharField(max_length=50)),
            ],
        ),
    ]
