# Generated by Django 5.1.1 on 2024-10-06 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
    ]
