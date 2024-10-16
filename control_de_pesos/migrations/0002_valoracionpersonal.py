# Generated by Django 5.1.1 on 2024-10-11 23:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mycoach', '0002_comentarioentrenamiento_delete_valoracionpersonal'),
        ('control_de_pesos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValoracionPersonal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_valoracion', models.DateField()),
                ('masa_segmental', models.DecimalField(decimal_places=2, max_digits=5)),
                ('grasa_corporal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mycoach.usuario')),
            ],
        ),
    ]
