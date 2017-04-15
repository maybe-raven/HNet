from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from account.models import Patient, Doctor, get_account_from_user
from .models import Drug, Diagnosis, Test
from .forms import DrugForm, DiagnosisForm, TestForm, TestResultsForm
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


@login_required
@permission_required('medical.request_test')
@user_passes_test(lambda u: not u.is_superuser)
def request_test(request, diagnosis_id):
    diagnosis = get_object_or_404(Diagnosis, pk=diagnosis_id)
    # Assigning None to doctor for some unknown reason
    doctor = get_account_from_user(request.user)

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
    patient = test.diagnosis.patient

    if request.method == 'POST':
        results_form = TestResultsForm(request.POST, instance=test)
        if results_form.is_valid():
            results_form.save()
            patient.medical_information = test.results
            patient.save()
            CreateLogEntry(request.user.username, "Test results uploaded.")
            return render(request, 'medical/test/uploaded.html')
    else:
        results_form = TestResultsForm
        return render(request, 'medical/test/upload.html', {'results_form': results_form, 'test': test})
