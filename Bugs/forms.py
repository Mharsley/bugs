from django import forms
from Bugs.models import Ticket


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class NewTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'Title',
            'Description'
        ]
