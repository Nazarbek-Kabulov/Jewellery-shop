from django import forms
from django.forms import CharField, TextInput, EmailField, EmailInput, Textarea
from multiupload.fields import MultiImageField


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.Form):
    title = forms.CharField(label='Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your product title'
    }))
    price = forms.FloatField(label='Price', widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    image = MultipleFileField()
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))


class CommentForm(forms.Form):
    name = CharField(widget=TextInput(attrs={
        'placeholder': 'Name',
        'class': 'main_text'
    }))
    email = EmailField(widget=EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'main_text'
    }))
    phone = CharField(widget=TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'main_text'
    }))
    message = CharField(widget=Textarea(attrs={
        'placeholder': 'Message',
        'class': 'message-bt',
        'rows': 5,
        'id': 'comment'
    }))
