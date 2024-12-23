from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()
        return user
    
from django import forms
from django.forms.models import inlineformset_factory
from .models import Event, Attachment

# Kreiraj inline formset za Attachment
AttachmentFormSet = inlineformset_factory(
    Event,
    Attachment,
    fields=['file'],
    extra=1,  # Po defaultu prikaži 1 prazan red za prilog
    can_delete=True  # Omogući korisniku da obriše priložene datoteke
)