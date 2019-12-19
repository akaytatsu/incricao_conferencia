# Generated by Django 2.2.6 on 2019-12-19 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_conferencia_pagseguro_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscricao',
            name='pagseguro_code',
            field=models.CharField(blank=True, max_length=120, verbose_name='Token PagSeguro'),
        ),
        migrations.AddField(
            model_name='inscricao',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pendente'), (2, 'Pago'), (3, 'Cancelado')], default=1, verbose_name='Status'),
        ),
    ]
