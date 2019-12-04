from django import forms

from apps.accounts.models import Account


# class ContactForm(forms.Form):
#     nome = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
#     mensagem = forms.CharField(widget=forms.Textarea, required=True)

# class CreateAccountForm(forms.ModelForm):

#     error_messages = {
#         'password_mismatch': "The two password fields didn't match.",
#     }

#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput, )
#     email = forms.EmailField()

#     class Meta:
#         model = Account
#         fields = ('email', 'name', )

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


class LoginForm(forms.Form):
    cpf = forms.CharField()
    data_nascimento = forms.DateField()
