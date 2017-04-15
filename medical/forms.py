from django import forms
from .models import Drug, Diagnosis


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
