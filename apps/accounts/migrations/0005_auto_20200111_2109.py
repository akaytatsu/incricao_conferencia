# Generated by Django 3.0.1 on 2020-01-11 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200106_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='can_pay',
            field=models.BooleanField(default=False, verbose_name='Pode Repassar Recurso?'),
        ),
        migrations.AddField(
            model_name='account',
            name='telefone',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True, verbose_name='Telefone'),
        ),
    ]
