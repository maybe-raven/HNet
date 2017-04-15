from django import forms
from .models import Drug, Prescription


class DrugForm(forms.ModelForm):
    """
    A form for obtaining information related to a drug.
    Can be used for adding new drugs as well as editing existing drugs.
    """

    class Meta:
        model = Drug
        fields = ['name', 'description']


class PrescriptionForm(forms.ModelForm):
    """
    A form for obtaining information related to a prescription.
    Can be used for adding new prescriptions.
    """

    class Meta:
        model = Prescription
        fields = ['diagnosis', 'doctor', 'drug', 'quantity', 'instruction']
