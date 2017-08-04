# By Zhufyak V.V
# zhufyakvv@gmail.com
# github.com/zhufyakvv
# 02.07.2017
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from pluto import models


class LogInForm(forms.Form):
    username = forms.CharField(label='Username')
    username.widget = forms.TextInput(attrs={'class': 'form-control'})
    password = forms.CharField(label='Password')
    password.widget = forms.PasswordInput(attrs={'class': 'form-control'})


class PersonalInfoForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    first_name.widget = forms.TextInput(attrs={'class': 'form-control'})
    last_name = forms.CharField(label='Last Name')
    last_name.widget = forms.TextInput(attrs={'class': 'form-control'})


class PersonalImageForm(forms.Form):
    image = forms.ImageField(label='Personal image')
    image.widget = forms.FileInput(attrs={'class': 'form-control'})


class PasswordForm(forms.Form):
    password = forms.CharField(label='Password')
    password.widget = forms.PasswordInput(attrs={'class': 'form-control'})
    password_confirm = forms.CharField(label='Password confirm')
    password_confirm.widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password_confirm")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match."
            )


# TODO Make it DRY
class SignUpForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=128)
    email.widget = forms.TextInput(attrs={'class': 'form-control'})
    username = forms.CharField(label='Username')
    username.widget = forms.TextInput(attrs={'class': 'form-control'})
    password = forms.CharField(label='Password')
    password.widget = forms.PasswordInput(attrs={'class': 'form-control'})
    password_confirm = forms.CharField(label='Password confirm')
    password_confirm.widget = forms.PasswordInput(attrs={'class': 'form-control'})

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password_confirm")

        try:
            models.User.objects.get(username=username)
            raise forms.ValidationError(
                "User already exist."
            )
        except ObjectDoesNotExist:
            pass

        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "User with this email already exist."
            )
        except ObjectDoesNotExist:
            pass

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match."
            )
