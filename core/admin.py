from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *

admin.site.site_header = "Adota Pet Admin"


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        """_summary_
        """
        model = User
        fields = ('email',)

    def clean_password2(self):
        """_summary_

        Raises:
            forms.ValidationError: _description_

        Returns:
            _type_: _description_
        """

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """_summary_

        Args:
            commit (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        """_summary_
        """
        model = User
        fields = ('email', 'password', 'is_admin')

    def clean_password(self):
        """# Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        """

        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    """
    The forms to add and change user instances

    # form = UserChangeForm
    add_form = UserCreationForm
    """

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'nome')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': (
            'email',
            'password',
            'is_active',
            'nome')
        }),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Personal info', {'fields': (
            'cpf',
            'celular'
        )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
