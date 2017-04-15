from django.shortcuts import render
from hnet.logger import readLog
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AdmissionForm


@login_required()
@permission_required('account.view_log')
def logView(request):
    log = readLog()
    return render(request, 'hospital/viewlog.html', {"log": log})


@login_required
@permission_required('hospital.admit_patient')
def admit_patient(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'hospital/admission_done.html')
    else:
        form = AdmissionForm()

    return render(request, 'hospital/admit_patient.html', {'form': form})
