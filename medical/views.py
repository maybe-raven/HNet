from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render
from .forms import DrugForm
from account.models import ProfileInformation, get_account_from_user, Patient
from medical.models import Prescription



@login_required
@permission_required('medical.add_drug')
def add_drug(request):
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'medical/drug/add_done.html')
    else:
        form = DrugForm()

    return render(request, 'medical/drug/add.html', {'form': form})


@login_required
@permission_required('medical.view_prescription')
@user_passes_test(lambda u: not u.is_superuser)
def view_prescriptions(request):
    patient = get_account_from_user(request.user)
    prescriptions = Prescription.objects.all()
    list_prescription = []
    for prescription in prescriptions:
        if prescription.diagnosis.treatment_session.patient == patient:
            list_prescription.append(prescription)
    context = {'prescription_list': list_prescription}
    return render(request, 'patient/patient_prescriptions.html', context)

@login_required
@permission_required('account.view_patients')
@user_passes_test(lambda u: not u.is_superuser)
def view_patients(request):
    nurse = get_account_from_user(request.user)
    hospital = nurse.hospital
    list_patients = []
    patients = Patient.objects.all()
    for patient in patients:
        if patient.preferred_hospital == hospital:
            list_patients.append(patient)

    context = {'patient_list': list_patients}

    return render(request, 'patient/view_patients.html', context)
