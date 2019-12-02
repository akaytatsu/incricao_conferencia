from django.db import models

# Create your models here.
class Conferencia(models.Model):

    titulo = models.CharField(max_length=80, verbose_name="Titulo")
    max_inscr = models.IntegerField(default=500000, verbose_name="Maximo inscrições")
    data_abertura = models.DateTimeField(verbose_name="Data Abertura Inscrições")
    data_encerramento = models.DateTimeField(verbose_name="Data Encerramento Inscrições")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conferencia"
        verbose_name = 'Conferencia'
        verbose_name_plural = 'Conferencias'

class Valores(models.Model):

    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE, verbose_name="Conferência")
    idade_inicial = models.IntegerField(default=0, verbose_name="Idade Inicial")
    idade_final = models.IntegerField(default=120, verbose_name="Idade Final")
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name="Valor Inscrição")

    class Meta:
        db_table = "valor_inscricao_conferencia"
        verbose_name = 'Valor Inscrição Conferencia'
        verbose_name_plural = 'Valores Inscrição Conferencia'

class inscricao(models.Model):

    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE, verbose_name="Conferência")
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    nome_cracha = models.CharField(max_length=100, verbose_name="Nome Crachá")
    data_nascimento = models.DateField(verbose_name="Data Nascimento")
    email = models.CharField(max_length=120, verbose_name="E-mail")
    # aaaaaaaa = models.CharField(max_length=120, verbose_name="aaaaaaaaaaaaaaaaaa")
    # aaaaaaaa = models.CharField(max_length=100, verbose_name="aaaaaaaaaaaaaaaaaa")
    # aaaaaaaa = models.CharField(max_length=100, verbose_name="aaaaaaaaaaaaaaaaaa")
    

    class Meta:
        db_table = "inscricao"
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'