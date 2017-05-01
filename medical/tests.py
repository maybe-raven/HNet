from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user
from django.contrib.auth.models import User, AnonymousUser
from medical.models import Test, Diagnosis
from django.core.urlresolvers import reverse
from medical.views import upload_test_result


# Create your tests here.


class uploadfiletest(TestCase):
    def setup(self):
        self.factory = RequestFactory()

    def test_upload_file(self):
        username = 'doctor'
        patientu = 'patient'
        password = '$teamname'
        doctor = User.objects.get(username=username).doctor
        patient = User.objects.get(username=patientu).patient
        diagnosis = Diagnosis.objects.create(patient=patient, summery=" ", catagory=" ")
        test = Test.objects.create(doctot=doctor, diagnosis=diagnosis, description="", results="", notes="")
        request = self.factory.post(reverse('medical:upload_test_result', args=[test.id]))
        response = self.client.post(reverse('account:register_patient'))
        self.assertEqual(response.status_code, 302, 'Expected to be redirected due to insufficient permission.')
