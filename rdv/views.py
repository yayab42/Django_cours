import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView


@login_required()
def index(request):
    today = datetime.datetime.now()
    context = {}
    return render(request, 'rdv/index.html', context)


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
