import datetime
from datetime import timedelta, datetime

import pytz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rdv.forms import RdvForm, DoctorForm
from rdv.models import Doctor, Rdv


@login_required()
def index(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            print(user)
        return redirect(f'appointment/{user.id}')
    else:
        form = DoctorForm()
    context = {'form': form}
    return render(request, 'rdv/index.html', context)


@login_required()
def appointment(request, doctor_id):
    web_socket = 'ws://' + request.get_host() +'/socket/'
    print(web_socket)
    doctor = Doctor.objects.get(id=doctor_id)
    rdv_duration = doctor.type_rdv.duration
    today = datetime.today()
    matin = []
    aprem = []
    heures_aprem = today.replace(hour=14, minute=0, second=0, microsecond=0)
    heures_matin = today.replace(hour=8, minute=0, second=0, microsecond=0)
    while heures_matin < today.replace(hour=12, minute=0, second=0, microsecond=0):
        matin.append(pytz.utc.localize(heures_matin).strftime('%b %d %Y %I:%M %p'))
        heures_matin += timedelta(minutes=rdv_duration)
    while heures_aprem < today.replace(hour=18, minute=0, second=0, microsecond=0):
        aprem.append(pytz.utc.localize(heures_aprem).strftime('%b %d %Y %I:%M %p'))
        heures_aprem += timedelta(minutes=rdv_duration)
    if request.method == 'POST':
        form = RdvForm(request.POST)
        if form.is_valid():
            start = datetime.strptime(request.POST['schedule'], '%b %d %Y %I:%M %p')
            end = start + timedelta(minutes=rdv_duration)
            Rdv.objects.create(doctor=doctor, patient=request.user.patient, start=start, end=end)
            if end <= start:
                raise ValidationError("L'heure de début doit être inférieure à l'heure de fin")
            return redirect('approved')
    else:
        form = RdvForm()
    context = {'form': form, 'doctor_id': doctor_id, 'matin': matin, 'aprem': aprem, 'web_socket': web_socket}
    return render(request, 'rdv/appointment.html', context)


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def post(self, request, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('rdv/index.html')
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('rdv/index.html')
        return render(request, self.template_name)


class LogoutView(TemplateView):
    template_name = 'rdv/login.html'

    def get(self, request, **kwargs):
        logout(request)
        return HttpResponseRedirect('registration/login.html')


def approved(request):
    context = {}
    return render(request, 'rdv/approved.html', context)
