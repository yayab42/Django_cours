from datetime import datetime

from django.forms import ModelForm
from rdv.models import Rdv, Doctor
from django import forms


# Create the form class.
class RdvForm(ModelForm):
    end = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.today())

    class Meta:
        model = Rdv
        exclude = ['patient', 'doctor', 'start']


class DoctorForm(forms.Form):
    user = forms.ModelChoiceField(queryset=Doctor.objects.all(), label="Praticien")
