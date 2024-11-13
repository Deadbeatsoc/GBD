# Generated by Django 5.1.1 on 2024-10-06 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contrasena', models.CharField(max_length=255)),
                ('rol', models.CharField(choices=[('Entrenador', 'Entrenador'), ('Deportista', 'Deportista')], max_length=20)),
                ('edad', models.IntegerField()),
                ('sexo', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], max_length=10)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=4)),
                ('fecha_nacimiento', models.DateField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
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