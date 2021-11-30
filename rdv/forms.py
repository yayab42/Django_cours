from django.forms import ModelForm, DateInput
from rdv.models import Rdv
from django import forms


# Create the form class.
class RdvForm(ModelForm):
    date: forms.DateTimeField(widget=forms.DateTimeInput)

    class Meta:
        model = Rdv
        fields = ['start', 'doctor']
        exclude = ['type']

