from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, inlineformset_factory
from app.utils import generate_bootstrap_widgets_for_all_fields

from . import (
    models
)


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'phone' or field_name == 'telefone':
                field.widget.attrs['class'] = 'form-control telefone phone'
            if field_name == 'cep' or field_name == 'postalcode':
                field.widget.attrs['class'] = 'form-control cep'


class MusicForm(BaseForm, ModelForm):
    class Meta:
        model = models.Music
        fields = ("id", "youtube_url", "chordInfo", "derivedKey", "derivedBpm", "barLength", "versionId", "chords")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Music)

    def __init__(self, *args, **kwargs):
        super(MusicForm, self).__init__(*args, **kwargs)


class ArtistForm(BaseForm, ):
    artist = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255)


class MusicFormToInline(BaseForm, ModelForm):
    class Meta:
        model = models.Music
        fields = ("id", "youtube_url", "chordInfo", "derivedKey", "derivedBpm", "barLength", "versionId")
        widgets = generate_bootstrap_widgets_for_all_fields(models.Music)

    def __init__(self, *args, **kwargs):
        super(MusicFormToInline, self).__init__(*args, **kwargs)


class SearchForm(BaseForm):
    musica = forms.CharField(max_length=255, label='Musica')


class NewUserForm(BaseForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, max_length=255)
    first_name = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(BaseForm):
    username = forms.CharField(required=True, max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())
