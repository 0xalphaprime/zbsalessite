# Generated by Django 4.1.5 on 2023-02-19 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_alter_invoice_billed_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='billed_on',
            field=models.DateTimeField(),
        ),
    ]
