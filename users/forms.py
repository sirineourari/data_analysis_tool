from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.utils.translation import gettext as _
STATUS_CHOICES = (
    (1, _('Enseignant')),
    (2, _('Responsable module')),
    (3, _('Chef de departement')),
    (4, _('Administrateur')))


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    status =forms.ChoiceField(choices=STATUS_CHOICES, label="", initial='', widget=forms.Select(), required=True)
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2','status']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Identifiant'
        self.fields['email'].label = 'Adresse Email'
        self.fields['status'].label = 'Position'
        self.fields['password1'].label = 'Mot de passe '
        self.fields['password2'].label='Confirmation de mot de passe'


    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email existe")
       return self.cleaned_data

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    status =forms.ChoiceField(choices=STATUS_CHOICES, label="", initial='', widget=forms.Select(), required=True)
    class Meta:
        model =User
        fields =['username', 'email','status']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model =Profile
        fields =['image']
class UploadFileForm(forms.Form):
    file = forms.FileField()
