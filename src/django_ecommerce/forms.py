from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'Enter Full Name'
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Email',
        'class': 'form-control'
    }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)

        if qs.exists():
            raise forms.ValidationError('Username is Taken')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError('A user With The Same Email Exists')

        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if confirm_password != password:
            raise forms.ValidationError("Passwords Do Not Match")

        return data
