from django import forms
from .models import TreatmentSession


class AdmissionForm(forms.ModelForm):
    """
    Form for obtaining information related to admission
    can be used for admitting new patients.
    """

    class Meta:
        model = TreatmentSession
        fields = ['patient','treating_hospital', 'discharge_timestamp', 'previous_session', 'notes']
