# Generated by Django 5.1.1 on 2024-10-16 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mycoach', '0002_comentarioentrenamiento_delete_valoracionpersonal'),
        ('control_de_pesos', '0003_alter_nutricion_carbohidratos_alter_nutricion_grasas_and_more'),
        ('rutinas', '0003_ejercicio_nutricion_tiporutina_usuario_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ComentarioEntrenamiento',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]