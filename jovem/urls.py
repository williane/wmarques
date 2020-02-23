from django.urls import path, include
from .views import index, profile, acompanhar_status, form_user, indicacao

urlpatterns = [
    path('', index, name='index'),
    path('perfil/', profile, name='profile'),
    path('acompanhar_status/', acompanhar_status, name='acompanhar_status'),
    path('form_user/', form_user, name='form_user'),
    path('indicacao/', indicacao, name='indicacao'),
]