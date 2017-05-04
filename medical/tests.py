from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user
from django.contrib.auth.models import User, AnonymousUser, Group
from medical.models import Test, Diagnosis
from django.core.urlresolvers import reverse
from medical.views import upload_test_result
from django.core.files.uploadedfile import SimpleUploadedFile
from account.models import create_default_account, Patient, Doctor
from hospital.models import Hospital


# Create your tests here.


class uploadfiletest(TestCase):
    def setup(self):
        self.factory = RequestFactory()

    def test_upload_file(self):
        username = 'doctor'
        patientu = 'patient'
        password = '$teamname'
        hospital = Hospital.create_default()
        Group.objects.create(name='Patient')
        Group.objects.create(name='Doctor')
        create_default_account(username,password,Doctor, hospital)
        create_default_account(patientu,password,Patient, hospital)
        doctor = User.objects.get(username=username).doctor
        patient = User.objects.get(username=patientu).patient
        diagnosis = Diagnosis.objects.create(patient=patient)
        test = Test.objects.create(doctor=doctor, diagnosis=diagnosis, description="", results=SimpleUploadedFile('file.txt',b'test file'))
        response = self.client.post(reverse('medical:upload_test_result', args=[test.id]))
        print(response.status_code)
        self.assertEqual(response.status_code, 302, 'Expected to upload test result.')