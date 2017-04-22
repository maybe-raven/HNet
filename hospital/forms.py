from django import forms
from .models import TreatmentSession


class TransferForm(forms.ModelForm):
    """
    A form for obtaining the hospital a patient should be transferred to.
    """

    class Meta:
        model = TreatmentSession
        fields = ['treating_hospital']
