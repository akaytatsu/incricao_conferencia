# Generated by Django 2.2.6 on 2019-12-21 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0016_conferencia_inscricoes_abertas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospedagem',
            name='nome',
            field=models.CharField(max_length=60, verbose_name='Nome Hospedagem'),
        ),
    ]
