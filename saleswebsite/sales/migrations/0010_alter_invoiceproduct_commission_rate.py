# Generated by Django 4.1.5 on 2023-02-19 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_alter_invoiceproduct_commission_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceproduct',
            name='commission_rate',
            field=models.IntegerField(),
        ),
    ]
