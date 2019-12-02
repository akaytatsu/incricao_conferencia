from django.contrib import admin
from apps.accounts.models import Account
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

class CustomUserAdmin(UserAdmin):
    model = Account


# admin.site.unregister(Account)

admin.site.register(Account, CustomUserAdmin)
