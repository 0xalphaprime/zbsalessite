# Generated by Django 4.1.5 on 2023-02-19 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_alter_invoiceproduct_extended_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceproduct',
            name='commission_rate',
            field=models.FloatField(),
        ),
    ]
