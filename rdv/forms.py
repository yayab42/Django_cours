from django.forms import ModelForm
from rdv.models import Rdv


# Create the form class.
class RdvForm(ModelForm):
    class Meta:
        model = Rdv
        fields = ['date', 'doctor', 'type', 'duration']
