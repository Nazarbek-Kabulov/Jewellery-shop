from django.forms import Form, ModelForm, CharField, TextInput, PasswordInput, Textarea, EmailField, EmailInput


class RegisterForm(Form):
    first_name = CharField(label='First name', widget=TextInput(attrs={'id': 'first_name'}))
    last_name = CharField(label='Last name', widget=TextInput(attrs={'id': 'last_name'}))
    email = EmailField(label='Email', widget=EmailInput(attrs={'id': 'email'}))
    username = CharField(label='Username', widget=TextInput(attrs={'id': 'username'}))
    password = CharField(label='Password', widget=PasswordInput(attrs={'id': 'password'}))
    password_confirm = CharField(label='Password Confirm', widget=PasswordInput(attrs={'id': 'password_confirm'}))


class LoginForm(Form):
    username = CharField(label='Username', widget=TextInput(attrs={'id': 'username'}))
    password = CharField(label='Password', widget=PasswordInput(attrs={'id': 'password'}))
