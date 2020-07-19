from django.db import models


class RelatorioCidade(models.Model):
    class Meta:
        db_table = "relatorio_cidade"
        verbose_name = 'Relatório por Cidade'
        verbose_name_plural = 'Relatório por Cidades'


class RelatorioIdade(models.Model):
    class Meta:
        db_table = "relatorio_idade"
        verbose_name = 'Relatório por Idade'
        verbose_name_plural = 'Relatório por Idades'


class RelatorioStatusPagamento(models.Model):
    class Meta:
        db_table = "relatorio_status_pag"
        verbose_name = 'Relatório Status Pagamento'
        verbose_name_plural = 'Relatório Status Pagamento'


class RelatorioIdadeEspecifico(models.Model):
    class Meta:
        db_table = "relatorio_idade_especifico"
        verbose_name = 'Relatório por Idade Especifico'
        verbose_name_plural = 'Relatório por Idades Especificas'


class RelatorioHospedagem(models.Model):
    class Meta:
        db_table = "relatorio_hospedagem"
        verbose_name = 'Relatório por Hospedagem'
        verbose_name_plural = 'Relatório por Hospedagem'


class RelatorioCracha(models.Model):
    class Meta:
        db_table = "relatorio_cach"
        verbose_name = 'Relatório para Cracha'
        verbose_name_plural = 'Relatórios para Crachas'
