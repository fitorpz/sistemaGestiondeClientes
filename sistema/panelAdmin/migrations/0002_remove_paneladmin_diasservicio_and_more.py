# Generated by Django 4.2.5 on 2024-01-13 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panelAdmin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paneladmin',
            name='diasServicio',
        ),
        migrations.RemoveField(
            model_name='paneladmin',
            name='fechaVencimiento',
        ),
        migrations.RemoveField(
            model_name='paneladmin',
            name='plan',
        ),
    ]
