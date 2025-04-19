# Generated by Django 5.2 on 2025-04-19 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food", "0004_item_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="item_image",
            field=models.ImageField(blank=True, null=True, upload_to="food_images/"),
        ),
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.CharField(
                choices=[
                    ("fast_food", "Fast Food"),
                    ("main_course", "Main Course"),
                    ("drinks", "Drinks"),
                ],
                default="fast_food",
                max_length=20,
            ),
        ),
    ]
