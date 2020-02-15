from django.db import models
from apps.accounts.models import Account
from datetime import date, datetime
import pytz
utc=pytz.UTC

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def busca_valor(idade, conferencia):
    valor = Valores.objects.filter(conferencia=conferencia)
    valor = valor.filter(idade_inicial__lte=idade)
    valor = valor.filter(idade_final__gte=idade)

    if valor.exists():
        valor = valor.first()
        return valor.valor
    
    return 0

# Create your models here.
class Conferencia(models.Model):

    titulo = models.CharField(max_length=80, verbose_name="Titulo", help_text="Titulo do Evento")
    titulo_slug = models.SlugField(verbose_name="Slug", unique=True, help_text="Esse campo é o codigo unico da conferencia, não alterar esse campo")
    max_inscr = models.IntegerField(default=500000, verbose_name="Maximo inscrições")
    data_abertura = models.DateTimeField(verbose_name="Data Abertura Inscrições")
    data_encerramento = models.DateTimeField(verbose_name="Data Encerramento Inscrições")
    data_cadastro = models.DateTimeField(auto_now_add=True)
    endereco = models.CharField(max_length=320, blank=True, verbose_name="Endereço (googlemaps)")
    informacoes = models.TextField(blank=True, verbose_name="Informações Gerais")
    inscricoes_abertas = models.BooleanField(default=True, verbose_name="Inscrições Abertas?")
    informacoes_arquivo = models.FileField(upload_to="informacoes/arquivos/", null=True, blank=True, verbose_name="Arquivo de Informações")

    class Meta:
        db_table = "conferencia"
        verbose_name = 'Conferencia'
        verbose_name_plural = 'Conferencias'

    def __str__(self):
        return self.titulo
    
    def informacoes_as_html(self):
        return self.informacoes.replace("\n", "<br>")

    def total_inscricoes(self):
        total_inscricoes = Inscricao.objects.filter(conferencia=self).count()
        total_dependentes = Dependente.objects.filter(inscricao__conferencia=self).count()

        return total_inscricoes + total_dependentes

    def is_active(self):
        if self.total_inscricoes() >= self.max_inscr:
            return False
        
        if self.inscricoes_abertas is False:
            return False

        now_dt = datetime.now()

        if self.data_abertura.replace(tzinfo=None) > now_dt or self.data_encerramento.replace(tzinfo=None) < now_dt:
            return False

        return True

    @staticmethod
    def get_all_active():
        conferencias = []

        queryset = Conferencia.objects.all()

        for conf in queryset:
            if conf.is_active():
                conferencias.append(conf)

        return conferencias


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
    nome = models.CharField(max_length=60, verbose_name="Nome Hospedagem")
    limite = models.IntegerField(default=0, verbose_name="Limite de Hospedes")
    ativo = models.BooleanField(default=True, verbose_name="Ativo?")

    class Meta:
        db_table = "hospedagem_conferencia"
        verbose_name = 'Hospedagem Conferência'
        verbose_name_plural = 'Hospedagem Conferência'

    def __str__(self):
        return "{}".format(self.nome)

class Inscricao(models.Model):

    _STATUS = (
        (1, 'Pendente'),
        (2, 'Pago'),
        (3, 'Cancelado'),
        (4, 'Aguardando Confirmação Pagamento'),
    )

    conferencia = models.ForeignKey(Conferencia, on_delete=models.DO_NOTHING, verbose_name="Conferência")
    usuario = models.ForeignKey(Account, null=False, blank=False, verbose_name="Usuario", on_delete=models.DO_NOTHING)
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    nome_cracha = models.CharField(max_length=100, verbose_name="Nome Crachá", blank=True)
    data_nascimento = models.DateField(verbose_name="Data Nascimento")
    email = models.CharField(max_length=120, verbose_name="E-mail")
    cep = models.CharField(max_length=9, verbose_name="CEP")
    endereco = models.CharField(max_length=120, verbose_name="Endereço")
    numero = models.CharField(max_length=60, verbose_name="Numero")
    complemento = models.CharField(max_length=60, verbose_name="Complemento", blank=True)
    bairro = models.CharField(max_length=80, verbose_name="Bairro")
    cidade = models.CharField(max_length=80, verbose_name="Cidade")
    uf = models.CharField(max_length=2, verbose_name="UF")
    ddd = models.CharField(max_length=3, verbose_name="DDD")
    telefone = models.CharField(max_length=30, verbose_name="Telefone")
    observacoes = models.CharField(max_length=400, verbose_name="Observações", blank=True)
    hospedagem = models.ForeignKey(Hospedagem, on_delete=models.DO_NOTHING, verbose_name="Hospedagem")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Inscrição", default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total Inscrição", default=0)
    idade = models.IntegerField(default=0, verbose_name="Idade")
    pagseguro_code = models.CharField(max_length=120, verbose_name="Token PagSeguro", blank=True)
    payment_reference = models.CharField(max_length=120, verbose_name="Referencia Pagamento", blank=True)
    status = models.IntegerField(choices=_STATUS, default=1, verbose_name="Status")
    sit_pagseguro = models.IntegerField(verbose_name="Status PagSeguro", blank=True, null=True)
    pagseguro_transaction_id = models.CharField(max_length=120, verbose_name="Transação PagSeguro", blank=True, null=True)
    hospedagem_detalhe = models.CharField(max_length=120, null=False, blank=True, default="", verbose_name="Detalhe Hospedagem")
    
    class Meta:
        unique_together = [['conferencia', 'cpf']]
        db_table = "inscricao"
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'

    def __str__(self):
        return "{} - {}".format(self.conferencia, self.nome)

    def save(self, *args, **kwargs):
        self.idade = self.calc_idade()
        self.valor = busca_valor(self.idade, self.conferencia)

        try:
            self.nome = self.nome.upper()
        except:
            pass

        try:
            self.nome_cracha = self.nome_cracha.upper()
        except:
            pass

        try:
            self.endereco = self.endereco.upper()
        except:
            pass

        try:
            self.complemento = self.complemento.upper()
        except:
            pass

        try:
            self.bairro = self.bairro.upper()
        except:
            pass

        try:
            self.cidade = self.cidade.upper()
        except:
            pass

        try:
            self.uf = self.uf.upper()
        except:
            pass

        try:
            self.observacoes = self.observacoes.upper()
        except:
            pass

        super(Inscricao, self).save(*args, **kwargs)

        self.replicateHost()

    def replicateHost(self):
        if len(self.hospedagem_detalhe) > 3:
            for dep in Dependente.objects.filter(inscricao=self):
                if dep.hospedagem_detalhe == "":
                    dep.hospedagem_detalhe = self.hospedagem_detalhe
                    dep.save()
    
    def unmask(self, value):

        options = ["/", "-", " ", ".", ",", "_", "(", ")", "$", "*"]
        
        for op in options:
            value = value.replace(op, "")

        return value

    def cleanned_cpf(self):
        return self.unmask( self.cpf )

    def cleanned_cep(self):
        return self.unmask( self.cep )

    def cleanned_telefone(self):
        return self.unmask( self.telefone )

    def create_account(self):
        try:
            user = Account.objects.get(email=self.email)
        except Account.DoesNotExist:
            user = Account()
            user.name = self.nome
            user.email = self.email
            user.username = self.cleanned_cpf()
            user.save()
            user.set_password("{}".format(self.cleanned_cpf))
            user.save()

        self.usuario = user
        
        return user
    
    def calc_idade(self):
        return calculate_age(self.data_nascimento)
    
    def num_dependentes(self):
        return Dependente.objects.filter(inscricao=self).count()

    def atualiza_valor_total(self):
        self.valor_total = self.busca_valor_total()
        self.save()

    def busca_valor_total(self):
        total = 0
        total = self.valor

        dependentes = Dependente.objects.filter(inscricao=self)

        for dep in dependentes:
            dep.atualiza_valor_total()
            total = total + dep.valor
        
        return total
    
    def status_display(self):
        for g in self._STATUS:
            if g[0] == self.status:
                return g[1]
        
        return ""


class Dependente(models.Model):

    _GRAU = (
        (1, 'Conjugue'),
        (2, 'Filho(a)'),
        (3, 'Pai/Mãe'),
        (4, 'Outro'),
    )

    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE, verbose_name="Inscrição")
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    grau = models.IntegerField(choices=_GRAU, verbose_name="Grau Parentesco")
    nome_cracha = models.CharField(max_length=100, verbose_name="Nome Crachá", blank=True)
    data_nascimento = models.DateField(verbose_name="Data Nascimento")
    idade = models.IntegerField(default=0, verbose_name="Idade")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Inscrição", default=0)
    hospedagem_detalhe = models.CharField(max_length=120, null=False, blank=True, default="", verbose_name="Detalhe Hospedagem")

    class Meta:
        db_table = "dependente"
        verbose_name = 'Dependente'
        verbose_name_plural = 'Dependentes'

    def __str__(self):
        return "{} - {} - {}".format(self.inscricao, self.grau, self.nome)
    
    def save(self, *args, **kwargs):
        self.idade = self.calc_idade()
        
        try:
            self.nome = self.nome.upper()
        except:
            pass
        
        try:
            self.nome_cracha = self.nome_cracha.upper()
        except:
            pass

        super(Dependente, self).save(*args, **kwargs)

        self.inscricao.save()
    
    def calc_idade(self):
        return calculate_age(self.data_nascimento)
    
    def atualiza_valor_total(self):
        self.valor = busca_valor(self.idade, self.inscricao.conferencia)
        self.save()
    
    def grau_display(self):
        for g in self._GRAU:
            if g[0] == self.grau:
                return g[1]
        
        return ""

class Contato(models.Model):

    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE, verbose_name="Conferência")
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE, verbose_name="Inscrição")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    email = models.CharField(max_length=120, verbose_name="Email")
    assunto = models.CharField(max_length=120, verbose_name="Assunto")
    data_contato = models.DateTimeField(auto_now_add=True, verbose_name="Data Contato")
    descricao = models.TextField(verbose_name="Descrição")
    
    class Meta:
        db_table = "contato"
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'

    def __str__(self):
        return "{} - {}".format(self.conferencia.titulo, self.nome)