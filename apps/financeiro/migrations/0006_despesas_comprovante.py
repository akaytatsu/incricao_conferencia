# Generated by Django 3.0.1 on 2020-01-14 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0005_despesas_data_solicitacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesas',
            name='comprovante',
            field=models.ImageField(blank=True, null=True, upload_to='comprovantes/'),
        ),
    ]
