from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def marketoverview(request):
    return render(request, 'marketoverview.html')
