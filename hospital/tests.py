from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser
from account.management.commands import setupgroups
from account.models import Patient, Doctor, Nurse, create_default_account
from hospital.models import Hospital, TreatmentSession
from hospital import views

PATIENT_USERNAME = 'patient'
DOCTOR_USERNAME = 'doctor'
NURSE_USERNAME = 'nurse'
PASSWORD = '$teamname'


class PatientAdmissionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        setupgroups.Command().handle()

        hospital = Hospital.objects.create()
        create_default_account(PATIENT_USERNAME, PASSWORD, Patient, hospital)
        create_default_account(DOCTOR_USERNAME, PASSWORD, Doctor, hospital)
        create_default_account(NURSE_USERNAME, PASSWORD, Nurse, hospital)

    def setUp(self):
        self.factory = RequestFactory()

    def test_doctor_successful(self):
        patient = User.objects.get(username=PATIENT_USERNAME).patient
        request = self.factory.post(reverse('hospital:admit_patient', args=[patient.id]), {})
        request.user = User.objects.get(username=DOCTOR_USERNAME)
        views.admit_patient(request, patient.id)

        self.assertTrue(TreatmentSession.objects.exists(), 'Expected a new treatment session to be created.')
        treatment_session = TreatmentSession.objects.first()
        self.assertEqual(treatment_session.patient, patient,
                         'Expected the new treatment session to be associated with the given patient.')
        self.assertEqual(treatment_session.discharge_timestamp, None, 'Unexpected discharge for patient.')

    def test_nurse_successful(self):
        patient = User.objects.get(username=PATIENT_USERNAME).patient
        request = self.factory.post(reverse('hospital:admit_patient', args=[patient.id]), {})
        request.user = User.objects.get(username=NURSE_USERNAME)
        views.admit_patient(request, patient.id)

        self.assertTrue(TreatmentSession.objects.exists(), 'Expected a new treatment session to be created.')
        treatment_session = TreatmentSession.objects.first()
        self.assertEqual(treatment_session.patient, patient,
                         'Expected the new treatment session to be associated with the given patient.')
        self.assertEqual(treatment_session.discharge_timestamp, None, 'Unexpected discharge for patient.')

    def test_failed_permission(self):
        patient_user = User.objects.get(username=PATIENT_USERNAME)
        patient = patient_user.patient
        request = self.factory.post(reverse('hospital:admit_patient', args=[patient.id]), {})
        request.user = AnonymousUser()
        response = views.admit_patient(request, patient.id)

        self.assertEqual(response.status_code, 302, 'Expected to be redirected due to insufficient permission.')
        self.assertFalse(TreatmentSession.objects.exists(), 'Expected failing to create new treatment session.')

        request = self.factory.post(reverse('hospital:admit_patient', args=[patient.id]), {})
        request.user = patient_user
        response = views.admit_patient(request, patient.id)

        self.assertEqual(response.status_code, 302, 'Expected to be redirected due to insufficient permission.')
        self.assertFalse(TreatmentSession.objects.exists(), 'Expected failing to create new treatment session.')

    def test_failed_already_admitted(self):
        patient = User.objects.get(username=PATIENT_USERNAME).patient
        request = self.factory.post(reverse('hospital:admit_patient', args=[patient.id]), {})
        request.user = User.objects.get(username=DOCTOR_USERNAME)
        views.admit_patient(request, patient.id)
        views.admit_patient(request, patient.id)

        self.assertEqual(TreatmentSession.objects.count(), 1, 'Expected skipping treatment session creation.')
