# Generated by Django 3.0.1 on 2020-01-06 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='tp_user_financeiro',
            field=models.IntegerField(choices=[(0, 'Nenhum'), (1, 'Solicitante'), (2, 'Aprovador'), (3, 'Super')], default=0, verbose_name='Tipo Usuario Financeiro'),
        ),
    ]
