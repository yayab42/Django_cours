from django.forms import ModelForm
from rdv.models import Rdv, Doctor, Patient
from django import forms


# Create the form class.
class RdvForm(ModelForm):
    date: forms.DateTimeField(widget=forms.DateTimeInput)

    class Meta:
        model = Rdv
        fields = ['start']
        exclude = ['type', 'doctor']


class DoctorForm(forms.Form):
    user = forms.ModelChoiceField(queryset=Doctor.objects.all(), label="Praticien")

