from django.urls import path
from . import views
from dashapp.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('', views.home, name='dashapp-home'),
    path('dashapp-dashboard', views.dashboard, name='dashapp-dashboard')

]