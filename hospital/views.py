from django.shortcuts import render
from hnet.logger import readLog

def logView(request):
    log = readLog()
    return render(request, 'hospital/viewlog.html', {"log": log})