# Generated by Django 5.2.2 on 2025-07-11 01:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_ticketsale_agent'),
        ('users', '0002_remove_agent_user_agent_commission_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketsale',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.agent'),
        ),
    ]
