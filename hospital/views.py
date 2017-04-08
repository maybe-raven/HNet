from django.shortcuts import render


def logView(request):
    return render(request, 'hospital/viewlog.html')