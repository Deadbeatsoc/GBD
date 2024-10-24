# Generated by Django 5.1.1 on 2024-10-21 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutinas', '0004_rutina_duracion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('especialidad', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Deportista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('edad', models.IntegerField()),
                ('deporte', models.CharField(max_length=100)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deportistas', to='rutinas.coach')),
            ],
        ),
    ]
