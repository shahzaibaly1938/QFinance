# Generated by Django 5.2.2 on 2025-07-03 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_ticketsale_commission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketsale',
            name='agent',
        ),
    ]
