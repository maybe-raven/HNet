from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import Group

from .models import Patient, ProfileInformation
from .fields import PhoneField


class UserCreationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])

        return user

    def save_as_patient_with_profile_information(self, patient_form, profile_information_form):
        user = self.save()
        patient_group = Group.objects.get(name='Patient')
        user.groups.add(patient_group)
        user.save()

        profile_information = profile_information_form.save(commit=False)
        profile_information.account_type = ProfileInformation.PATIENT
        profile_information.user = user
        profile_information.save()

        patient = patient_form.save(commit=False)
        patient.user = user
        patient.save()

        return user


class ProfileInformationForm(forms.ModelForm):
    phone = PhoneField()

    class Meta:
        model = ProfileInformation
        fields = ['gender', 'address', 'phone']


class PatientCreationForm(forms.ModelForm):
    emergency_contact_phone = PhoneField(required=False,
                                         help_text='The phone number of an unregistered emergency contact. You must provide this if you do not link with a registered patient.')

    def clean(self):
        cleaned_data = super(PatientCreationForm, self).clean()

        if 'emergency_contact' in cleaned_data and 'emergency_contact_phone' in cleaned_data:
            if cleaned_data['emergency_contact'] is None and not cleaned_data['emergency_contact_phone']:
                self.add_error('emergency_contact_phone',
                               'If you choose not to link with a registered patient account, you must provide an emergency contact phone number.')

        return cleaned_data

    class Meta:
        model = Patient
        fields = ['medical_information', 'preferred_hospitals', 'proof_of_insurance', 'emergency_contact',
                  'emergency_contact_phone']


class PatientChangeForm(PatientCreationForm):
    def clean_emergency_contact(self):
        if self.instance is not None:
            if self.instance == self.cleaned_data['emergency_contact']:
                raise forms.ValidationError('Your emergency contact cannot be yourself.')

        return self.cleaned_data['emergency_contact']
