from django.db import models
from hospital.models import Hospital, TreatmentSession
from django.contrib.auth.models import User


class ProfileInformation(models.Model):
    """
    A model that describes the basic profile information of a user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_information')

    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    PATIENT = 'P'
    ADMINISTRATOR = 'A'
    DOCTOR = 'D'
    NURSE = 'N'

    ACCOUNT_TYPE_CHOICES = (
        (PATIENT, 'Patient'),
        (ADMINISTRATOR, 'Administrator'),
        (DOCTOR, 'Doctor'),
        (NURSE, 'Nurse'),
    )

    account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPE_CHOICES)

    address = models.CharField(max_length=80)
    phone = models.CharField(max_length=10)

    @classmethod
    def from_user(cls, user):
        """
        Attempt to get the profile information of the given user.
        :return: The profile information if it exist; otherwise, None.
        """
        try:
            return user.profile_information
        except (ProfileInformation.DoesNotExist, AttributeError):
            return None


class AbstractUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        abstract = True


class Patient(AbstractUser):
    preferred_hospital = models.ForeignKey(Hospital, related_name='+')

    medical_information = models.TextField(blank=True)

    proof_of_insurance = models.TextField()

    emergency_contact = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT,
                                          help_text='You have the option to link with a registered patient '
                                                    'as an emergency contact.')
    emergency_contact_phone = models.CharField(max_length=10, null=True, blank=True,
                                               help_text='The phone number of an unregistered emergency contact. '
                                                         'You must provide this if you do not '
                                                         'link with a registered patient.')


class Administrator(AbstractUser):
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT)


class Doctor(AbstractUser):
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT)

    treatment_sessions = models.ManyToManyField(TreatmentSession, blank=True)


class Nurse(AbstractUser):
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT)

    treatment_sessions = models.ManyToManyField(TreatmentSession, blank=True)


def get_account_from_user(user):
    """
    Get the correct account object associated with the given user, or None if it doesn't have an associated account object.
    The account object is one of four types: `Patient`, `Administrator`, `Doctor`, or `Nurse`.
    :param user: A User object.
    :return:
    """

    profile_information = ProfileInformation.from_user(user)
    if profile_information is not None:
        if profile_information.account_type == ProfileInformation.PATIENT:
            return user.patient
        elif profile_information.account_type == ProfileInformation.DOCTOR:
            return user.doctor
        elif profile_information.account_type == ProfileInformation.NURSE:
            return user.nurse
        elif profile_information.account_type == ProfileInformation.ADMINISTRATOR:
            return user.administrator
