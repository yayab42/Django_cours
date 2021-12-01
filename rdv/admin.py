from django.contrib import admin
from rdv.models import Doctor, Patient, Rdv, TypeRdv

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Rdv)
admin.site.register(TypeRdv)
