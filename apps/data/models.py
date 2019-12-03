from django.db import models

# Create your models here.
class Conferencia(models.Model):

    titulo = models.CharField(max_length=80, verbose_name="Titulo")
    titulo_slug = models.SlugField(verbose_name="Slug", unique=True)
    max_inscr = models.IntegerField(default=500000, verbose_name="Maximo inscrições")
    data_abertura = models.DateTimeField(verbose_name="Data Abertura Inscrições")
    data_encerramento = models.DateTimeField(verbose_name="Data Encerramento Inscrições")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conferencia"
        verbose_name = 'Conferencia'
        verbose_name_plural = 'Conferencias'

    def __str__(self):
        return self.titulo

class Valores(models.Model):

    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE, verbose_name="Conferência")
    idade_inicial = models.IntegerField(default=0, verbose_name="Idade Inicial")
    idade_final = models.IntegerField(default=120, verbose_name="Idade Final")
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name="Valor Inscrição")

    class Meta:
        db_table = "valor_inscricao_conferencia"
        verbose_name = 'Valor Inscrição Conferencia'
        verbose_name_plural = 'Valores Inscrição Conferencia'

    def __str__(self):
        return "{} - R$ {} de {} a {}".format(self.conferencia, self.valor, self.idade_inicial, self.idade_final)

class Hospedagem(models.Model):

    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE, verbose_name="Conferência")
    nome = models.CharField(max_length=9, verbose_name="Nome Hospedagem")
    limite = models.IntegerField(default=0, verbose_name="Limite de Hospedes")
    ativo = models.BooleanField(default=True, verbose_name="Ativo?")

    class Meta:
        db_table = "hospedagem_conferencia"
        verbose_name = 'Hospedagem Conferência'
        verbose_name_plural = 'Hospedagem Conferência'

    def __str__(self):
        return "{} - {}".format(self.conferencia, self.nome)

class Inscricao(models.Model):

    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE, verbose_name="Conferência")
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    nome_cracha = models.CharField(max_length=100, verbose_name="Nome Crachá")
    data_nascimento = models.DateField(verbose_name="Data Nascimento")
    email = models.CharField(max_length=120, verbose_name="E-mail")
    cep = models.CharField(max_length=9, verbose_name="CEP")
    endereco = models.CharField(max_length=120, verbose_name="Endereço")
    numero = models.CharField(max_length=60, verbose_name="Numero")
    complemento = models.CharField(max_length=60, verbose_name="Complemento")
    bairro = models.CharField(max_length=80, verbose_name="Bairro")
    cidade = models.CharField(max_length=80, verbose_name="Cidade")
    uf = models.CharField(max_length=2, verbose_name="UF")
    ddd = models.CharField(max_length=3, verbose_name="DDD")
    telefone = models.CharField(max_length=30, verbose_name="Telefone")
    observacoes = models.CharField(max_length=400, verbose_name="Observações")
    hospedagem = models.ForeignKey(Hospedagem, on_delete=models.CASCADE, verbose_name="Hospedagem")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Inscrição")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total Inscrição")
    idade = models.IntegerField(default=0, verbose_name="Idade")
    
    class Meta:
        unique_together = [['conferencia', 'cpf']]
        db_table = "inscricao"
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'

    def __str__(self):
        return "{} - {} - {}".format(self.conferencia, self.cpf, self.nome)

class Dependente(models.Model):

    _GRAU = (
        (1, 'Conjugue'),
        (2, 'Filho(a)'),
        (3, 'Pai/Mãe'),
        (4, 'Outro'),
    )

    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE, verbose_name="Inscrição")
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    grau = models.CharField(choices=_GRAU, max_length=30, verbose_name="Grau Parentesco")
    nome_cracha = models.CharField(max_length=100, verbose_name="Nome Crachá")
    data_nascimento = models.DateField(verbose_name="Data Nascimento")
    idade = models.IntegerField(default=0, verbose_name="Idade")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Inscrição")

    class Meta:
        db_table = "dependente"
        verbose_name = 'Dependente'
        verbose_name_plural = 'Dependentes'

    def __str__(self):
        return "{} - {} - {}".format(self.inscricao, self.grau, self.nome)
