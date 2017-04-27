from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from account.models import Patient, get_account_from_user
from hospital.models import TreatmentSession, Statistics, Hospital
from .models import Drug, Diagnosis, Test, Prescription
from .forms import DrugForm, DiagnosisForm, TestForm, TestResultsForm, PrescriptionForm
from medical.models import Prescription
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


@permission_required('medical.add_prescription')
@user_passes_test(lambda u: not u.is_superuser)
def add_prescription(request, diagnosis_id):
    diagnosis = get_object_or_404(Diagnosis, pk=diagnosis_id)
    Statistics.add_prescription(Hospital.statistics)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save_to_diagnosis_by_doctor(diagnosis, request.user.doctor)
            return render(request, 'medical/prescriptions/add_done.html', {'diagnosis_id': diagnosis_id})
    else:
        form = PrescriptionForm()

    return render(request, 'medical/prescriptions/add.html', {'form': form, 'diagnosis_id': diagnosis_id})


@permission_required('medical.change_prescription')
@user_passes_test(lambda u: not u.is_superuser)
def edit_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)

    doctor = request.user.doctor
    if prescription.doctor != doctor:
        raise PermissionDenied('Cannot edit prescriptions created by another doctor.')

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return render(request, 'medical/prescriptions/edit.html', {'form': form, 'message': 'All changes saved.'})
    else:
        form = PrescriptionForm(instance=prescription)

    return render(request, 'medical/prescriptions/edit.html', {'form': form})


@permission_required('medical.delete_prescription')
@user_passes_test(lambda u: not u.is_superuser)
def remove_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)

    doctor = request.user.doctor
    if prescription.doctor != doctor:
        raise PermissionDenied('Cannot delete prescriptions created by another doctor.')

    if request.method == 'POST':
        diagnosis_id = prescription.diagnosis.id
        prescription.delete()
        return render(request, 'medical/prescriptions/remove_done.html', {'diagnosis_id': diagnosis_id})

    return render(request, 'medical/prescriptions/remove.html', {'prescription': prescription})


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


@permission_required('medical.change_drug')
@user_passes_test(lambda u: not u.is_superuser)
def update_drug(request, drug_id):
    drug = get_object_or_404(Drug, pk=drug_id)
    if not drug.active:
        raise Http404()

    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
        if form.is_valid():
            form.save()
            return render(request, 'medical/drug/update.html', {'form': form, 'message': 'All changes saved.'})
    else:
        form = DrugForm(instance=drug)

    return render(request, 'medical/drug/update.html', {'form': form})


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

    return render(request, 'medical/patient/medical_information.html', {
        'medical_information': medical_information, 'patient': patient,
        'user_has_edit_permission': request.user.has_perm('medical.change_diagnosis'),
        'user_has_add_permission': request.user.has_perm('medical.add_diagnosis')
    })


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
            return render(request, 'medical/test/requested.html', {'diagnosis_id': diagnosis_id})
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
            return render(request, 'medical/test/uploaded.html', {'test': test})
    else:
        results_form = TestResultsForm(instance=test)

    return render(request, 'medical/test/upload.html', {'results_form': results_form, 'test': test})


@permission_required('medical.release_test_results')
@user_passes_test(lambda u: not u.is_superuser)
def release_test_result(request, test_id):
    test = get_object_or_404(Test, pk=test_id)

    if request.method == 'POST':
        test.released = True
        test.save()
        return render(request, 'medical/test/release_done.html', {'diagnosis_id': test.diagnosis.id})

    return render(request, 'medical/test/release.html', {'test': test})
