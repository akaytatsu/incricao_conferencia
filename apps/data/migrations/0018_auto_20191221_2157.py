# Generated by Django 2.2.6 on 2019-12-21 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0017_auto_20191221_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscricao',
            name='pagseguro_transaction_id',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Transação PagSeguro'),
        ),
    ]
