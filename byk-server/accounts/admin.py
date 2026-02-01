# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

from django import forms
from django.contrib import admin
from .models import User, Tenant, DjangoUser


class UserAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True,
                               help_text="Enter the user's password.")
    internal_user = forms.ModelChoiceField(queryset=DjangoUser.objects.all(), required=False,
                                           help_text="Select the internal Django user associated with this user.")
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.all(), required=False,
                                    help_text="Select the tenant for the user.")

    class Meta:
        model = User
        exclude = ["password_hash"]

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.create_password(password)
        if commit:
            user.save()
        return user


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "created_at", "updated_at")
    search_fields = ("username", "email")
    ordering = ("-created_at",)
    form = UserAdminForm


class TenantAdmin(admin.ModelAdmin):
    list_display = ("slug", "name")



admin.site.register(User, UserAdmin)
admin.site.register(Tenant, TenantAdmin)
