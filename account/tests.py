from django.test import TestCase
from hospital.models import Hospital
from account.models import ProfileInformation
from account.forms import ProfileInformationForm, PatientCreationForm


# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        Hospital.objects.create(name='Test hospital', location='Test location')

    def test_patient_creation_success(self):
        profile_info = ProfileInformationForm({'gender': ProfileInformation.FEMALE, 'address': '416 River St.', 'phone': '8784563456'})
        create_patient = PatientCreationForm({'emergency_contact_phone': '5153453230', 'medical_information': 'allergies',
                                              'preferred_hospital': Hospital.objects.first().id, 'proof_of_insurance': '12233455'})

        self.assertTrue(profile_info.is_valid(), 'Profile information form should pass validation.')
        self.assertTrue(create_patient.is_valid(), 'Patient form should pass validation.')

    def test_patient_creation_empty_fields(self):
        profile_info = ProfileInformationForm({'gender': '', 'address': '', 'phone': ''})
        create_patient = PatientCreationForm({'emergency_contact_phone': '', 'medical_information': '', 'preferred_hospital': '', 'proof_of_insurance': ''})

        self.assertFalse(profile_info.is_valid(), 'Profile information form should fail validation.')
        self.assertFalse(create_patient.is_valid(), 'Patient form should fail validation.')

        profile_info_errors = profile_info.errors
        self.assertTrue('gender' in profile_info_errors, 'Required field not reporting an error when no value is supplied.')
        self.assertTrue('address' in profile_info_errors, 'Required field not reporting an error when no value is supplied.')
        self.assertTrue('phone' in profile_info_errors, 'Required field not reporting an error when no value is supplied.')

        patient_errors = create_patient.errors
        self.assertTrue('preferred_hospital' in patient_errors, 'Required field not reporting an error when no value is supplied.')
        self.assertTrue('proof_of_insurance' in patient_errors, 'Required field not reporting an error when no value is supplied.')
        self.assertTrue('emergency_contact_phone' in patient_errors, 'Required field not reporting an error when no value is supplied.')
