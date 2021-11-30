from django.contrib import admin
from rdv.models import Person, Rdv, TypeRdv

admin.site.register(Person)
admin.site.register(Rdv)
admin.site.register(TypeRdv)