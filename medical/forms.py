from django import forms
from .models import Drug, Diagnosis, Test
from account.models import Patient


class DrugForm(forms.ModelForm):
    """
    A form for obtaining information related to a drug.
    Can be used for adding new drugs as well as editing existing drugs.
    """

    class Meta:
        model = Drug
        fields = ['name', 'description']


class DiagnosisForm(forms.ModelForm):
    def save_for_patient(self, patient):
        diagnosis = self.save(commit=False)
        diagnosis.patient = patient
        diagnosis.save()

        return diagnosis

    class Meta:
        model = Diagnosis
        fields = ['summary']


class TestForm(forms.ModelForm):
    """
    A form for obtaining information for a medical test.
    """

    def save_for_diagnosis(self, doctor, diagnosis):
        test = self.save(commit=False)
        test.doctor = doctor
        test.diagnosis = diagnosis
        test.save()

        return test

    class Meta:
        model = Test
        fields = ['description']


class TestResultsForm(forms.ModelForm):
    """
    A form for obtaining test results in text form.
    """

    class Meta:
        model = Test
        fields = ['results']
