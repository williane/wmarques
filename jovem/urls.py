from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index, profile, acompanhar_status, form_user, indicacao, form_instituicao, instituicao_list
from .views import usuario_list, usuario_update, instituicao_update, indicado_update, send_email, form_resetpassword

urlpatterns = [
    path('', index, name='index'),
    path('perfil/', profile, name='profile'),
    path('acompanhar_status', acompanhar_status, name='acompanhar_status'),
    path('form_user/', form_user, name='form_user'),
    path('form_instituicao/', form_instituicao, name='form_instituicao'),
    path('indicacao/<int:id>/<slug:nome>', indicacao, name='indicacao'),
    path('instituicao/', instituicao_list, name='instituicao_list'),
    path('usuario/', usuario_list, name='usuario_list'),
    path('usuario_update/<int:id>', usuario_update, name='usuario_update'),
    path('instituicao_update/<int:id>', instituicao_update, name='instituicao_update'),
    path('indicado_update/<int:id>', indicado_update, name='indicado_update'),
    path('send_email', send_email, name='send_email'),
    path('passwordReset', form_resetpassword, name='form_resetpassword'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)