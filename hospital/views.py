from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Patient, get_account_from_user
from hospital.models import TreatmentSession, Statistics, Hospital
from hnet.logger import CreateLogEntry, readLog


@login_required
@permission_required('hospital.add_treatmentsession')
@user_passes_test(lambda u: not u.is_superuser)
def admit_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    Statistics.add_patient(Hospital.statistics)
    if request.method == 'POST':
        if patient.get_current_treatment_session() is None:
            hospital = get_account_from_user(request.user).hospital
            TreatmentSession.objects.create(patient=patient, treating_hospital=hospital)
            CreateLogEntry(request.user.username, "Patient admitted.")

    return redirect('medical:view_medical_information', patient_id=patient_id)


@login_required
@permission_required('hospital.discharge_patient')
@user_passes_test(lambda u: not u.is_superuser)
def discharge_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    session = patient.get_current_treatment_session()

    if session is None:
        return redirect('medical:view_medical_information', patient_id=patient_id)

    if request.method == 'POST':
        if session.diagnosis_set.count() == 0:
            session.delete()
        else:
            session.discharge_timestamp = datetime.now()
            session.save()

        CreateLogEntry(request.user.username, "Patient discharged.")
        return render(request, 'discharge/discharge_done.html', {'patient_id': patient_id})
    else:
        return render(request, 'discharge/discharge.html', {'session': session})


def logView(request):
    log = readLog()
    return render(request, 'hospital/viewlog.html', {"log": log})

@login_required()
def statisticsView(request):
    return render(request, 'hospital/viewstatistics.html')
