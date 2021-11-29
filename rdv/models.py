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
