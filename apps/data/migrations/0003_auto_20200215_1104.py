# Generated by Django 3.0.3 on 2020-02-15 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20200203_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependente',
            name='hospedagem_detalhe',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='Detalhe Hospedagem'),
        ),
        migrations.AddField(
            model_name='inscricao',
            name='hospedagem_detalhe',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name='Detalhe Hospedagem'),
        ),
    ]
