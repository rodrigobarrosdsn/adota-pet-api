# Generated by Django 4.2.1 on 2023-10-17 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_animal_sexo'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='imagem_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='animal_images/'),
        ),
    ]