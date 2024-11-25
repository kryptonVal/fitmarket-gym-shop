# Generated by Django 5.1.3 on 2024-11-24 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymstore', '0004_product_is_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_featured',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]