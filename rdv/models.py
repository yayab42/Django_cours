from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime


# class Person(models.Model):
#     def __str__(self):
#         return self.user.username
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     CATEGORY_CHOICES = (
#         ("MEDECIN", "Medecin"),
#         ("PATIENT", "Patient")
#     )
#     category = models.CharField(max_length=8,
#                                 choices=CATEGORY_CHOICES,
#                                 default="Patient")


class Patient(models.Model):
    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Doctor(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User, on_delete=models.CASCADE)


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
    type = models.ForeignKey(TypeRdv, null=True, on_delete=models.CASCADE, related_name='type')
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name='patient')
    start = models.DateTimeField(default=datetime.now, help_text="Jour et heure du rendez-vous")
    end = models.DateTimeField(default=datetime.now, help_text="Fin du rendez-vous")

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:
            overlap = False
        elif (fixed_start <= new_start <= fixed_end) or (fixed_start <= new_end <= fixed_end):
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:
            overlap = True

        return overlap

    def clean(self):
        if self.end <= self.start:
            raise ValidationError("L'heure de début doit être inférieure à l'heure de fin")

        events = Rdv.objects.filter(start=self.start)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start, self.end):
                    raise ValidationError(
                        'Il y a déjà un rendez vous à : ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))

    def __str__(self):
        return str(self.start)
