from django.db import models

class RelatorioCidade(models.Model):
    class Meta:
        db_table = "relatorio_cidade"
        verbose_name = 'Relatório por Cidade'
        verbose_name_plural = 'Relatório por Cidades'