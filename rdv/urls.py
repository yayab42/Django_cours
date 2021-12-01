from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from . import views

urlpatterns = [
    path('', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('index/', views.index, name='index'),
    path('appointment/<int:doctor_id>', views.appointment, name='appointment'),
    path('approved/', views.approved, name='approved'),
]
