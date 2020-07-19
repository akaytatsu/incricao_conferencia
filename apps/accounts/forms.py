from django import forms


class LoginForm(forms.Form):
    cpf = forms.CharField()
    data_nascimento = forms.DateField()
