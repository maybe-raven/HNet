from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Patient, get_account_from_user
from hospital.models import TreatmentSession, Statistics
from hnet.logger import CreateLogEntry, readLog
from hospital.forms import TransferForm


@login_required
@permission_required('hospital.add_treatmentsession')
@user_passes_test(lambda u: not u.is_superuser)
def admit_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        if patient.get_current_treatment_session() is None:
            hospital = get_account_from_user(request.user).hospital
            TreatmentSession.objects.create(patient=patient, treating_hospital=hospital)
            Statistics.add_patient(Statistics.objects.get(name=hospital.name + " Statistics"))
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


@login_required
@permission_required('hospital.view_system_information')
def logView(request, page=0):
    logs = readLog()

    page = int(page)
    start = page * 20
    end = (page + 1) * 20

    total = len(logs)
    has_prev = page > 0
    prev = page - 1 if has_prev else None
    next = page + 1 if end < total else None

    logs = logs[start:end]
    return render(request, 'hospital/viewlog.html',
                  {"log_list": logs, 'has_prev': has_prev, 'prev': prev, 'next': next})


@login_required
@permission_required('hospital.view_system_information')
def statisticsView(request):
    from account.models import Administrator
    user = request.user
    hospital_name = Administrator.objects.get(user=user).hospital.name
    print("\n" + hospital_name + " Statistics\n")
    Statistics.find_appointments(Statistics.objects.get(name=hospital_name + " Statistics"))
    Statistics.find_doctors(Statistics.objects.get(name=hospital_name + " Statistics"))
    Statistics.find_nurses(Statistics.objects.get(name=hospital_name + " Statistics"))
    Statistics.calculate_avarage_length_of_stay(Statistics.objects.get(name=hospital_name + " Statistics"))
    Statistics.calculate_avarage_visit_per_patient(Statistics.objects.get(name=hospital_name + " Statistics"))
    stats_string = Statistics.__str__(Statistics.objects.get(name=hospital_name + " Statistics"))
    stats = stats_string.split("\n")
    return render(request, 'hospital/viewstatistics.html', {"stats": stats})


@login_required
@permission_required('hospital.transfer_patient_any_hospital')
@user_passes_test(lambda u: not u.is_superuser)
def transfer_patient_as_admin(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    session = patient.get_current_treatment_session()

    if session is None:
        return render(request, 'transfer/not_admitted.html', {'patient_id': patient_id})

    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            session.discharge_timestamp = datetime.now()
            session.save()
            form.save_by_admin(patient, session)
            CreateLogEntry(request.user.username, "Patient transferred.")
            return render(request, 'transfer/transfer_done_admin.html', {'patient_id': patient_id})
    else:
        form = TransferForm()

    return render(request, 'transfer/admin_transfer.html', {'form': form})


@login_required
@permission_required('hospital.transfer_patient_receiving_hospital')
@user_passes_test(lambda u: not u.is_superuser)
def transfer_patient_as_doctor(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    session = patient.get_current_treatment_session()

    if session is None:
        return redirect('medical:view_medical_information', patient_id=patient_id)

    if session.treating_hospital is get_account_from_user(request.user).hospital:
        return render(request, 'transfer/cant_transfer.html')

    if request.method == 'POST':
        session.discharge_timestamp = datetime.now()
        session.save()
        hospital = get_account_from_user(request.user).hospital
        new_session = TreatmentSession.objects.create(patient=patient, treating_hospital=hospital)
        new_session.previous_session = session
        new_session.save()
        CreateLogEntry(request.user.username, "Patient transferred.")
        return render(request, 'transfer/transfer_done.html', {'patient_id': patient_id})

    return render(request, 'transfer/doctor_transfer.html')


@login_required()
@permission_required('hospital.view_system_information')
def system_information(request):
    return render(request, 'hospital/system_information.html')
