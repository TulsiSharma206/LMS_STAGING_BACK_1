# Generated by Django 3.1.1 on 2020-11-11 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_paymentinfo_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'verbose_name': 'Batches', 'verbose_name_plural': 'Batches'},
        ),
        migrations.AlterModelOptions(
            name='contactus',
            options={'verbose_name': 'contact Us', 'verbose_name_plural': 'contact Us'},
        ),
        migrations.AlterModelOptions(
            name='enroll',
            options={'verbose_name': 'Enroll', 'verbose_name_plural': 'Enroll'},
        ),
        migrations.AlterModelOptions(
            name='paymentinfo',
            options={'verbose_name': 'Payment Info', 'verbose_name_plural': 'Payment Info'},
        ),
    ]
