# Generated by Django 3.1a1 on 2024-08-09 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_auto_20240809_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='historial',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
