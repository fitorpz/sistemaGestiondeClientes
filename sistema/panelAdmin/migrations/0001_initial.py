# Generated by Django 4.2.5 on 2024-01-10 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='panelAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuenta', models.CharField(max_length=10)),
                ('contraseña', models.CharField(max_length=10)),
                ('fechaInicio', models.DateTimeField(auto_now_add=True)),
                ('fechaUltimoPago', models.DateTimeField(blank=True, null=True)),
                ('plan', models.CharField(max_length=20)),
                ('fechaVencimiento', models.DateTimeField()),
                ('diasServicio', models.IntegerField()),
            ],
        ),
    ]
