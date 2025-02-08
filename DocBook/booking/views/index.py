from django.shortcuts import render

def index(request):
    return render(request, 'booking/index.html')