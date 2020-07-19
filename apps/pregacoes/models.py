from django.db import models


class Local(models.Model):

    nome = models.CharField(max_length=120, verbose_name="Nome do Local", null=False, blank=False)
    endereco = models.CharField(max_length=230, verbose_name="Endereço do Local")

    class Meta:
        db_table = "pregacao_local"
        verbose_name = 'Local Pregação'
        verbose_name_plural = 'Locais de Pregação'

    def __str__(self):
        return "{}".format(self.nome)


class Preletor(models.Model):

    nome = models.CharField(max_length=120, verbose_name="Nome do Local", null=False, blank=False)
    localidade = models.CharField(max_length=120, verbose_name="Localidade Preletor", null=True, blank=True)

    class Meta:
        db_table = "pregacao_preletor"
        verbose_name = 'Preletor'
        verbose_name_plural = 'Preletores'

    def __str__(self):
        return "{}".format(self.nome)


class ArquivoReferencia(models.Model):

    pregacao = models.ForeignKey('pregacoes.Pregacao', verbose_name="Pregação",
                                 on_delete=models.CASCADE, related_name="pregacao_arquivo_referencia")
    nome = models.CharField(max_length=120, verbose_name="Nome do Arquivo Referencia", null=False, blank=False)
    arquivo = models.FileField(upload_to='pregacoes/arquivos/', null=False, blank=False)

    class Meta:
        db_table = "pregacao_arquivos"
        verbose_name = 'Arquivo Pregação'
        verbose_name_plural = 'Arquivos de Pregações'

    def __str__(self):
        return "{}".format(self.nome)


class Pregacao(models.Model):

    titulo = models.CharField(max_length=120, verbose_name="Titulo", null=False, blank=False)
    preletor = models.ForeignKey(Preletor, on_delete=models.CASCADE, verbose_name="Preletor")
    local = models.ForeignKey(Local, on_delete=models.DO_NOTHING, verbose_name="Local da Pregação")
    data_pregacao = models.DateField(verbose_name="Data da Pregação",)
    resumo = models.TextField(verbose_name="Resumo Pregação", null=True, blank=True)

    class Meta:
        db_table = "pregacao_pregacao"
        verbose_name = 'Pregação'
        verbose_name_plural = 'Pregações'

    def __str__(self):
        return "{}/{}".format(self.titulo, self.preletor.nome)
