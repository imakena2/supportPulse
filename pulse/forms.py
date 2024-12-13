from django import forms
from .models import Ticket, Response
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name",
        }),
        required=True,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Your Email",
        }),
        required=True,
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Subject",
        }),
        required=True,
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Message",
            "rows": 6,
        }),
        required=True,
    )
    
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['phone', 'subject', 'description', 'issue']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'issue': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['response_text']

class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['response']
        

