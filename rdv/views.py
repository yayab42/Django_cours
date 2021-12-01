import datetime
from datetime import timedelta, timezone

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rdv.forms import RdvForm, DoctorForm
from rdv.models import Doctor, Rdv, Patient
import pytz



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
    doctor = Doctor.objects.get(id=doctor_id)
    rdv_duration = doctor.type_rdv.duration
    utc = pytz.UTC
    if request.method == 'POST':
        form = RdvForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = start + timedelta(minutes=rdv_duration)
            Rdv.objects.create(doctor=doctor, patient=request.user.patient, start=start, end=end)
            return redirect('approved')
    else:
        form = RdvForm()
    context = {'form': form, 'doctor_id': doctor_id}
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
