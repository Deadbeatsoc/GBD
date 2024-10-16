# Generated by Django 5.1.1 on 2024-10-16 23:12

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutinas', '0002_delete_comentarioentrenamiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ejercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ejercicio', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('tipo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Nutricion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_comida', models.CharField(max_length=100)),
                ('calorias', models.IntegerField()),
                ('proteinas', models.DecimalField(decimal_places=2, max_digits=5)),
                ('grasas', models.DecimalField(decimal_places=2, max_digits=5)),
                ('carbohidratos', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='TipoRutina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tipo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contrasena', models.CharField(max_length=255)),
                ('rol', models.CharField(choices=[('Administrador', 'Administrador'), ('Entrenador', 'Entrenador'), ('Deportista', 'Deportista')], max_length=20)),
                ('edad', models.IntegerField()),
                ('sexo', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], max_length=20)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fecha_nacimiento', models.DateField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='entrenamientoprincipal',
            name='rutina',
        ),
        migrations.RemoveField(
            model_name='estiramiento',
            name='rutina',
        ),
        migrations.AddField(
            model_name='rutina',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.CreateModel(
            name='RutinaCalentamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duracion_minutos', models.IntegerField()),
                ('repeticiones', models.IntegerField()),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.ejercicio')),
                ('rutina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.rutina')),
            ],
        ),
        migrations.CreateModel(
            name='RutinaEntrenamientoPrincipal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.IntegerField()),
                ('repeticiones', models.IntegerField()),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.ejercicio')),
                ('rutina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.rutina')),
            ],
        ),
        migrations.CreateModel(
            name='RutinaEstiramiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duracion_minutos', models.IntegerField()),
                ('repeticiones', models.IntegerField()),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.ejercicio')),
                ('rutina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.rutina')),
            ],
        ),
        migrations.AddField(
            model_name='rutina',
            name='tipo_rutina',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='rutinas.tiporutina'),
        ),
        migrations.CreateModel(
            name='ComentariosEntrenamientos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha_comentario', models.DateTimeField(auto_now_add=True)),
                ('rutina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.rutina')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.usuario')),
            ],
        ),
        migrations.AlterField(
            model_name='rutina',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.usuario'),
        ),
        migrations.CreateModel(
            name='ValoracionesPersonales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_valoracion', models.DateField()),
                ('grasa_corporal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('agua_corporal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('comentarios', models.TextField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='MasaSegmental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('musculo', models.CharField(choices=[('Brazo Derecho', 'Brazo Derecho'), ('Brazo Izquierdo', 'Brazo Izquierdo'), ('Pierna Derecha', 'Pierna Derecha'), ('Pierna Izquierda', 'Pierna Izquierda'), ('Tronco', 'Tronco')], max_length=100)),
                ('masa', models.DecimalField(decimal_places=2, max_digits=5)),
                ('valoracion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.valoracionespersonales')),
            ],
        ),
        migrations.DeleteModel(
            name='Calentamiento',
        ),
        migrations.DeleteModel(
            name='EntrenamientoPrincipal',
        ),
        migrations.DeleteModel(
            name='Estiramiento',
        ),
    ]
