
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render
from .forms import DrugForm
from account.models import ProfileInformation, get_account_from_user, Patient
from medical.models import Prescription


from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from account.models import Patient
from .models import Drug, Diagnosis
from .forms import DrugForm, DiagnosisForm
from hnet.logger import CreateLogEntry



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

  
@permission_required('medical.remove_drug')
@user_passes_test(lambda u: not u.is_superuser)
def remove_drug(request, drug_id):
    drug = get_object_or_404(Drug, pk=drug_id)

    if not drug.active:
        return render(request, 'medical/drug/already_removed.html')

    if request.method == 'POST':
        drug.active = False
        drug.save()
        CreateLogEntry(request.user.username, "Drug removed.")
        return render(request, 'medical/drug/remove_done.html')
    else:
        return render(request, 'medical/drug/remove.html', {'drug': drug})

      
@login_required
@permission_required('medical.add_diagnosis')
def create_diagnosis(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            diagnosis = form.save_for_patient(patient)
            return HttpResponseRedirect('%s?%s' % (
                reverse('medical:update_diagnosis', args=[diagnosis.id]),
                urlencode({'message': 'Diagnosis successfully created.'})
            ))
    else:
        form = DiagnosisForm()

    return render(request, 'medical/diagnosis/create.html',
                  {'patient': patient, 'form': form})


@login_required
@permission_required('medical.change_diagnosis')
def update_diagnosis(request, diagnosis_id):
    diagnosis = get_object_or_404(Diagnosis, pk=diagnosis_id)

    if request.method == 'POST':
        form = DiagnosisForm(request.POST, instance=diagnosis)
        if form.is_valid():
            form.save()
            return render(request, 'medical/diagnosis/update.html',
                          {'form': form, 'message': 'All changes saved.'})
    else:
        message = request.GET.get('message')
        form = DiagnosisForm(instance=diagnosis)

    return render(request, 'medical/diagnosis/update.html',
                  {'form': form, 'message': message})

