from cms.models import CMSPlugin
from django.db import models


class ColunaCMSPlugin(CMSPlugin):

    COLUMN_TYPE = [
        ['1', '1 Coluna'],
        ['2', '2 Colunas'],
        ['4', '4 Colunas'],
        ['6', '6 Colunas'],
        ['8', '8 Colunas'],
        ['10', '10 Colunas'],
        ['12', '12 Colunas'],
    ]

    coluna = models.CharField(max_length=10, choices=COLUMN_TYPE, verbose_name="Coluna")

    def __str__(self):
        return self.coluna
