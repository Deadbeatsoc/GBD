# Generated by Django 5.1.1 on 2024-10-16 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_de_pesos', '0002_valoracionpersonal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutricion',
            name='carbohidratos',
            field=models.DecimalField(decimal_places=2, default='', max_digits=5),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='grasas',
            field=models.DecimalField(decimal_places=2, default='', max_digits=5),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='nombre_comida',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='nutricion',
            name='proteinas',
            field=models.DecimalField(decimal_places=2, default='', max_digits=5),
        ),
        migrations.DeleteModel(
            name='ValoracionPersonal',
        ),
    ]