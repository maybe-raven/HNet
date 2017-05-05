from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Statistics(models.Model):
    name = models.CharField(max_length=30)
    num_of_patients = models.DecimalField(max_digits=999, decimal_places=3)
    avarage_visit_per_patient = models.DecimalField(max_digits=999, decimal_places=3)
    avarage_leangth_of_stay = models.DecimalField(max_digits=999, decimal_places=3)
    prescriptions_given = models.DecimalField(max_digits=999, decimal_places=3)

    def add_patient(self):
        self.num_of_patients += 1
        self.save()

    def add_prescription(self):
        self.prescriptions_given += 1
        self.save()

    def calculate_avarage_visit_per_patient(self):
        from account.models import Patient
        total_patients = Patient.objects.last().id
        self.avarage_visit_per_patient = self.num_of_patients / total_patients
        self.save()

    def __str__(self):
        string = ""
        string += "Number of patients visiting the hospital : " + str(self.num_of_patients) + "\n"
        string += "Avarage visits per patient : " + str(self.avarage_visit_per_patient) + "\n"
        string += "Avarage length of stay : " + str(self.avarage_leangth_of_stay) + "\n"
        string += "Number of prescriptions given : " + str(self.prescriptions_given) + "\n"
        return string


class Hospital(models.Model):
    """A model that describes the basic information of a hospital."""

    name = models.CharField(max_length=30)
    location = models.CharField(max_length=200)

    """A flag indicating whether or not this hospital is operational. Remove a hospital by setting this flag to False."""
    operational = models.BooleanField(default=True)

    statistics = models.ForeignKey(Statistics, on_delete=models.PROTECT)

    try:
        statistics = Statistics.objects.get(name="Statistics")
    except ObjectDoesNotExist:
        statistics = Statistics.objects.create(name="Statistics", num_of_patients=0, avarage_visit_per_patient=0
                                               , avarage_leangth_of_stay=0, prescriptions_given=0)

    def __str__(self):
        return self.name

    @staticmethod
    def create_default():
        return Hospital.objects.create(name='Test hospital', location='Test location')


class TreatmentSession(models.Model):
    """
    A model object that stores information of a patient's stay at a hospital.
    """

    patient = models.ForeignKey('account.Patient', on_delete=models.PROTECT)

    """The hospital at which the patient received his treatment."""
    treating_hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT)

    """The time when the patient was admitted to the hospital and started his treatment."""
    admission_timestamp = models.DateTimeField(auto_now_add=True)
    """The time when the treatment finished and the patient was discharged."""
    discharge_timestamp = models.DateTimeField(null=True, blank=True, default=None)

    """
    The patient may have received some treatment (possibly at another hospital) before this one.
    Reference to a treatment session before this one, if there is one; NULL, if there isn't.
    """
    previous_session = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True, default=None,
                                            related_name='next_session')

    """
    Any additional medical or non-medical notes about the patient that might help with any future treatment for this patient.
    """
    notes = models.TextField(blank=True)

    class Meta:
        permissions = (
            ('view_treatmentsession', 'Can view treatment sessions'),
            ('discharge_patient', 'Can discharge patient'),
        )
