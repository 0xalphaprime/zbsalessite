# Generated by Django 4.1.5 on 2023-02-19 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_rename_zimmer_id_customer_zimmer_cust_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='billed_on',
            field=models.DateField(blank=True, help_text='YYYY-MM-DD', null=True),
        ),
    ]
