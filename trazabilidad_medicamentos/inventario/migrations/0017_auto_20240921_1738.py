# Generated by Django 3.1a1 on 2024-09-21 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0016_auto_20240914_0737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forma_farmaceutica',
            name='via_administracion',
        ),
        migrations.AddField(
            model_name='forma_farmaceutica',
            name='via_administracion',
            field=models.ManyToManyField(to='inventario.Via_administracion'),
        ),
    ]