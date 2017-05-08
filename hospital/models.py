from django.db import models
from datetime import date, timedelta
from functools import reduce


def format_timedelta(delta):
    total_seconds = delta.seconds
    hours = total_seconds // 3600
    minutes = total_seconds % 3600 // 60
    seconds = total_seconds % 60

    return '{} days {:02}h {:02}m {:02}s'.format(delta.days, hours, minutes, seconds)


class Statistics(models.Model):
    def calculate(self):
        return ["Number of patients visiting the hospital : " + str(self.num_of_patients()),
                "Average visits per patient : " + str(self.average_visits_per_patient()),
                "Average length of stay : " + format_timedelta(self.average_length_of_stay()),
                "Number of prescriptions given : " + str(self.num_prescriptions_given()),
                "Number of Doctors : " + str(self.num_of_doctors()),
                "Number of Nurses : " + str(self.num_of_nurses()),
                "Appointments today : " + str(self.num_of_appointments_today())]

    def num_of_patients(self):
        from account.models import Patient
        treatment_session_query = TreatmentSession.objects.filter(discharge_timestamp=None).filter(treating_hospital=self.hospital)
        return Patient.objects.filter(treatmentsession__in=treatment_session_query).count()

    def num_of_doctors(self):
        from account.models import Doctor
        return Doctor.objects.filter(hospital=self.hospital).filter(user__is_active=True).count()

    def num_of_nurses(self):
        from account.models import Nurse
        return Nurse.objects.filter(hospital=self.hospital).filter(user__is_active=True).count()

    def num_of_appointments_today(self):
        from reservation.models import Appointment
        return Appointment.objects.filter(cancelled=False).filter(date=date.today()).filter(doctor__hospital=self.hospital).count()

    def average_visits_per_patient(self):
        treatment_session_query = TreatmentSession.objects.filter(treating_hospital=self.hospital)
        query_results = treatment_session_query.aggregate(
            visit_count=models.Count('id'),
            patient_count=models.Count('patient', distinct=True)
        )
        if query_results['patient_count'] == 0:
            return 0
        else:
            return query_results['visit_count'] / query_results['patient_count']

    def average_length_of_stay(self):
        treatment_session = TreatmentSession.objects.exclude(discharge_timestamp=None).filter(treating_hospital=self.hospital)
        if treatment_session.count() == 0:
            return timedelta()
        else:
            total_time = reduce(lambda acc, x: acc + (x.discharge_timestamp - x.admission_timestamp), treatment_session, timedelta())
            return total_time / treatment_session.count()

    def num_prescriptions_given(self):
        from medical.models import Prescription
        return Prescription.objects.filter(doctor__hospital=self.hospital).count()

    def __str__(self):
        return "Statistics for " + self.hospital.name

    class Meta:
        permissions = (
            ('can_view_system_information', 'Can view system information'),
        )


class Hospital(models.Model):
    """A model that describes the basic information of a hospital."""

    name = models.CharField(max_length=30)
    location = models.CharField(max_length=200)

    """A flag indicating whether or not this hospital is operational. Remove a hospital by setting this flag to False."""
    operational = models.BooleanField(default=True)

    statistics = models.OneToOneField(Statistics, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    @staticmethod
    def create_default():
        return Hospital.objects.create(name='Test hospital',
                                       statistics=Statistics.objects.create(
                                           num_of_patients=0,
                                           avarage_visit_per_patient=0,
                                           avarage_length_of_stay=0,
                                           prescriptions_given=0,
                                           num_of_doctors=0,
                                           num_of_nurses=0,
                                           appointments_that_day=0)
                                       , location='Test location')


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
            ('transfer_patient_any_hospital', 'Can transfer patient to any hospital'),
            ('transfer_patient_receiving_hospital', "Can transfer patient to user's hospital")
        )
