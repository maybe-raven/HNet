from django import forms
from .models import Drug


class DrugForm(forms.ModelForm):
    """
    A form for obtaining information related to a drug.
    Can be used for adding new drugs as well as editing existing drugs.
    """

    class Meta:
        model = Drug
        fields = ['name', 'description']
