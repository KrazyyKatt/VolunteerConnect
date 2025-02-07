from django import forms
from .models import *

# Registracija korisnika

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput) # Polje za validaciju unesene lozinke

    class Meta: # Ograničava formu na određena polja
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address')
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 250px;'}), # Postavljanje širine adrese kod registracije
        }

    def clean_password2(self): # Provjera lozinke ako je ista sa prvom
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    
    def save(self, commit=True): # Spremanje korisnika u bazu
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        user.is_staff = False
        user.is_superuser = False # Korisnici nisu admini

        if commit:
            user.save()
        return user


# Dodavanje priloga na objavu

from django.forms.models import inlineformset_factory

AttachmentFormSet = inlineformset_factory(
    Event,
    Attachment,
    fields=['file'],
    extra=1,  # Po defaultu prikaži 1 prazan red za prilog
    can_delete=False  # Onemogućeno brisanje priloženih datoteka
)