from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def profile(request):
    return render(request, 'profile.html')


def acompanhar_status(request):
    return render(request, 'acompanhar_status.html')


def form_user(request):
    return render(request, 'form_user.html')


def indicacao(request):
    return render(request, 'indicacao.html')

