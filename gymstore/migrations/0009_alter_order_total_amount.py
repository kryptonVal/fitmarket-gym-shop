# Generated by Django 5.1.3 on 2024-11-26 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymstore', '0008_alter_category_image_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]