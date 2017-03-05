from django.db import models
from account.models import Patient, Doctor


class Location(models.Model):
    """
    Represent a location within a hospital that can be used for an appointment
    E.g.: a doctor's office.
    """
    doctor = models.ForeignKey('account.Doctor', on_delete=models.PROTECT)

    """The location of this 'location' within a hospital"""
    location = models.CharField(max_length=20)

    """Is this location currently available for an appointment."""
    available = models.BooleanField(default=True)

    """
    Is this record still active?
    If an office is no longer used or assigned to a different doctor,
    set this flag to false rather than deleting or modifying this record to maintain data integrity,
    and create new record for the same physical location if necessary.
    """
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.location


class Appointment(models.Model):
    """
    A model object that stores an appointment's information.
    Replaced 'participants' variable in design document with 'doctor' and 'patient'.
    """
    title = models.CharField(max_length=50)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.view_appointment()

    def view_appointment(self):
        return "Doctor: " + self.doctor.__str__() + ".\nPatient: " + self.patient.__str__() + \
               ".\nDate: " + self.date.__str__() + \
               ".\nTime: " + self.start_time.__str__() + " - " + self.end_time.__str__() + "."

    def accessible_by_user(self, user):
        return self.patient.user == user or self.doctor.user == user

    class Meta:
        permissions = (
            ('cancel_appointment', 'Can cancel appointment'),
        )
