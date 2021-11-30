from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CATEGORY_CHOICES = (
        ("MEDECIN", "Medecin"),
        ("PATIENT", "Patient")
    )
    category = models.CharField(max_length=8,
                                choices=CATEGORY_CHOICES,
                                default="Patient")


class TypeRdv(models.Model):
    TYPE_CHOICES = (
        ("RDV SIMPLE", "Rdv simple"),
        ("RDV  SPECIALISTE", "Rdv spécialiste"),
        ("RDV AVEC MANIPULATION", "Rdv avec manipulation")
    )
    name = models.CharField(max_length=50,
                            choices=TYPE_CHOICES,
                            default="Rdv simple")
    DURATION_CHOICES = (
        (30, "30 min"),
        (45, "45 min"),
        (55, "55 min"),
    )
    duration = models.IntegerField(choices=DURATION_CHOICES)

    def __str__(self):
        return str(self.name)


class Rdv(models.Model):
    date = models.DateTimeField()
    type = models.ForeignKey(TypeRdv, null=True, on_delete=models.CASCADE, related_name='type')
    doctor = models.ForeignKey(Person, null=True, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(Person, null=True, on_delete=models.CASCADE, related_name='patient')

    def __str__(self):
        return str(self.date)


class Event(models.Model):

    day = models.DateTimeField('Jour du rendez-vous', help_text="Jour du rendez-vous")
    start = models.TimeField('Heure du rendez-vous', help_text="Heure du rendez-vous")
    end = models.TimeField('Heure du fin', help_text="Heure de fin")

    def __str__(self):
        return str(self)
