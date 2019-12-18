from django import forms

from .models import Inscricao, Hospedagem

class InscricaoForm(forms.ModelForm):

    _UF = [
        { "value": "", "label": "Selecione ..." },
        { "value": "AC", "label": "Acre" },
        { "value": "AL", "label": "Alagoas" },
        { "value": "AP", "label": "Amapá" },
        { "value": "AM", "label": "Amazonas" },
        { "value": "BA", "label": "Bahia" },
        { "value": "CE", "label": "Ceará" },
        { "value": "DF", "label": "Distrito Federal" },
        { "value": "GO", "label": "Goiás" },
        { "value": "ES", "label": "Espírito Santo" },
        { "value": "MA", "label": "Maranhão" },
        { "value": "MT", "label": "Mato Grosso" },
        { "value": "MS", "label": "Mato Grosso do Sul" },
        { "value": "MG", "label": "Minas Gerais" },
        { "value": "PA", "label": "Pará" },
        { "value": "PB", "label": "Paraiba" },
        { "value": "PR", "label": "Paraná" },
        { "value": "PE", "label": "Pernambuco" },
        { "value": "PI", "label": "Piauí­" },
        { "value": "RJ", "label": "Rio de Janeiro" },
        { "value": "RN", "label": "Rio Grande do Norte" },
        { "value": "RS", "label": "Rio Grande do Sul" },
        { "value": "RO", "label": "Rondônia" },
        { "value": "RR", "label": "Roraima" },
        { "value": "SP", "label": "São Paulo" },
        { "value": "SC", "label": "Santa Catarina" },
        { "value": "SE", "label": "Sergipe" },
        { "value": "TO", "label": "Tocantins" },
        { "value": "EX", "label": "Exterior" },
    ]

    uf = forms.ChoiceField(choices=[(doc.get("value"), doc.get("label")) for doc in _UF])
    email = forms.EmailField()

    class Meta:
        model = Inscricao
        exclude = ('idade', 'valor', 'valor_total', )

    def __init__(self, conferencia, *args, **kwargs):
        super(InscricaoForm, self).__init__(*args, **kwargs)
        self.fields['hospedagem'].queryset = Hospedagem.objects.filter(conferencia_id=conferencia, ativo=True)

    def clean_email(self):
        data = self.cleaned_data['email']

        if Inscricao.objects.filter(email=data, conferencia=self.data.get("conferencia")).count() > 0:
            raise forms.ValidationError("E-mail já cadastrado")
        return data

    def clean_cpf(self):
        data = self.cleaned_data['cpf']

        if Inscricao.objects.filter(cpf=data, conferencia=self.data.get("conferencia")).count() > 0:
            raise forms.ValidationError("CPF já cadastrado")
        return data