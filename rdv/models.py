from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CATEGORY_CHOICES = (
        ("MEDECIN", "Medecin"),
        ("PATIENT", "Patient")
    )
    category = models.CharField(max_length=8,
                                choices=CATEGORY_CHOICES,
                                default="Patient")


class Rdv (models.Model):
    date = models.DateTimeField()
    TYPE_CHOICES = (
        ("RDV SIMPLE", "Rdv simple"),
        ("RDV  SPECIALISTE", "Rdv spécialiste"),
        ("RDV AVEC MANIPULATION", "Rdv avec manipulation")
    )
    type = models.CharField(max_length=50,
                            choices=TYPE_CHOICES,
                            default="Rdv simple")
    DURATION_CHOICES = (
        (30, "30 min"),
        (45, "45 min"),
        (55, "55 min"),
    )
    duration = models.IntegerField(choices=DURATION_CHOICES)
    doctor = models.ForeignKey(Person, null=True, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(Person, null=True, on_delete=models.CASCADE, related_name='patient')
