from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from app.utils import generate_bootstrap_widgets_for_all_fields
from . import (
    models
)
from .models import SourceTrack, SourceFile


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone phone'
            if field_name == 'cep' or field_name == 'postalcode':
                field.widget.attrs['class'] = 'form-control cep'


class SourceTrackForm(BaseForm, ModelForm):
    class Meta:
        model = SourceTrack
        fields = ("user",)
        widgets = generate_bootstrap_widgets_for_all_fields(models.SourceTrack)

    def __init__(self, *args, **kwargs):
        super(SourceTrackForm, self).__init__(*args, **kwargs)


class SearchForm(BaseForm):
    musica = forms.CharField(max_length=255, label='Musica')


class NewUserForm(BaseForm, ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'],
                                        **{'first_name': validated_data['first_name']})
        return user


class LoginForm(BaseForm):
    username = forms.CharField(required=True, max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())


class UploadForm(BaseForm, ModelForm):
    class Meta:
        model = SourceFile
        fields = ['file']


class ProfileForm(BaseForm, ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]
