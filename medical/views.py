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
from hospital.models import TreatmentSession
from .models import Drug, Diagnosis, Test
from .forms import DrugForm, DiagnosisForm, TestForm, TestResultsForm
from hnet.logger import CreateLogEntry


@login_required
@permission_required('medical.view_drug')
@user_passes_test(lambda u: not u.is_superuser)
def list_drug(request):
    drug_list = Drug.objects.filter(active=True).order_by('name')

    return render(request, 'medical/drug/list.html', {'drug_list': drug_list})


@login_required
@permission_required('medical.add_drug')
@user_passes_test(lambda u: not u.is_superuser)
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
def view_prescriptions(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    prescriptions = Prescription.objects.all()
    list_prescription = []
    for prescription in prescriptions:
        if prescription.diagnosis.treatment_session.patient == patient:
            list_prescription.append(prescription)
    context = {'prescription_list': list_prescription, 'patient': patient}
    return render(request, 'patient/patient_overview.html', context)


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

    context = {'patient_list': list_patients, 'hospital': hospital}

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

@permission_required('medical.view_diagnosis')
@permission_required('hospital.view_treatmentsession')
def view_medical_information(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    medical_information = list(Diagnosis.objects.filter(patient=patient).filter(treatment_session=None))
    medical_information.extend(TreatmentSession.objects.filter(patient=patient))

    medical_information.sort(
        reverse=True,
        key=lambda item: item.creation_timestamp if isinstance(item, Diagnosis) else item.admission_timestamp
    )

    return render(request, 'medical/patient/medical_information.html',
                  {'medical_information': medical_information, 'patient': patient})


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


@login_required
@permission_required('medical.request_test')
@user_passes_test(lambda u: not u.is_superuser)
def request_test(request, diagnosis_id):
    diagnosis = get_object_or_404(Diagnosis, pk=diagnosis_id)
    doctor = request.user.doctor

    if doctor is None:
        return render(request, 'medical/test/requested.html')

    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            test_form.save_for_diagnosis(doctor, diagnosis)
            CreateLogEntry(request.user.username, "Test requested.")
            return render(request, 'medical/test/requested.html')
    else:
        test_form = TestForm()
        return render(request, 'medical/test/request.html', {'test_form': test_form, 'diagnosis': diagnosis})


@login_required()
@permission_required('medical.upload_test_results')
@user_passes_test(lambda u: not u.is_superuser)
def upload_test_result(request, test_id):
    test = get_object_or_404(Test, pk=test_id)

    if request.method == 'POST':
        results_form = TestResultsForm(request.POST, instance=test)
        if results_form.is_valid():
            results_form.save()
            CreateLogEntry(request.user.username, "Test results uploaded.")
            return render(request, 'medical/test/uploaded.html')
    else:
        results_form = TestResultsForm
        return render(request, 'medical/test/upload.html', {'results_form': results_form, 'test': test})
