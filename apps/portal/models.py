from cms.models import CMSPlugin
from django.db import models


class ColunaCMSPlugin(CMSPlugin):

    COLUMN_TYPE = [
        ['col-sm-12', '1 Coluna'],
        ['col-sm-6', '2 Colunas'],
        ['col-sm-4', '3 Colunas'],
        ['col-sm-3', '4 Colunas'],
        ['col-sm-2', '6 Colunas'],
    ]

    coluna = models.CharField(max_length=50, choices=COLUMN_TYPE, verbose_name="Coluna")

    def __str__(self):
        return self.coluna


class TituloPaginaCMSPlugin(CMSPlugin):

    titulo = models.CharField(max_length=120, verbose_name="Titulo")

    def __str__(self):
        return self.titulo


class TituloComponenteCMSPlugin(CMSPlugin):

    titulo = models.CharField(max_length=120, verbose_name="Titulo")

    def __str__(self):
        return self.titulo


class TextoComponenteCMSPlugin(CMSPlugin):

    texto = models.TextField(verbose_name="Texto")

    def __str__(self):
        return f'{self.pk}'


class TituloH3ComponenteCMSPlugin(CMSPlugin):

    titulo = models.CharField(max_length=120, verbose_name="Titulo")

    def __str__(self):
        return self.titulo
