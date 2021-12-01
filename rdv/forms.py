from django.forms import ModelForm
from rdv.models import Rdv, Person
from django import forms


# Create the form class.
class RdvForm(ModelForm):
    date: forms.DateTimeField(widget=forms.DateTimeInput)

    class Meta:
        model = Rdv
        fields = ['start', 'doctor']
        exclude = ['type']


class DoctorForm(forms.Form):
    user = forms.ModelChoiceField(queryset=Person.objects.filter(category='MEDECIN'), label="Praticien ")