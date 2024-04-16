# Generated by Django 5.0 on 2024-02-09 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('good_shop', '0007_remove_order_products_order_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='products',
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
