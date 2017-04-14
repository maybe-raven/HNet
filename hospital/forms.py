from django import forms
from .models import AdmitPatient


class AdmissionForm(forms.ModelForm):
    """
    Form for obtaining information related to admission
    can be used for admitting new patients.
    """

    class Meta:
        model = AdmitPatient
        fields = ['patient', 'reason']
