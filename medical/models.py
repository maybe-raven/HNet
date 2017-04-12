from django.db import models
from hospital.models import Hospital, TreatmentSession
from account.models import Doctor
from hnet.logger import CreateLogEntry


class DiagnosisCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Diagnosis(models.Model):
    treatment_session = models.OneToOneField(TreatmentSession, on_delete=models.CASCADE)

    """A high level summary of this patient's condition, including any useful, medical information for the treatment"""
    summary = models.TextField(blank=True)

    category = models.ManyToManyField(DiagnosisCategory, blank=True)


class Test(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.PROTECT)

    description = models.TextField()
    results = models.TextField()
    notes = models.TextField()

    timestamp = models.DateTimeField(auto_now=True)


class Drug(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()


class Prescription(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT)

    instruction = models.TextField()

    timestamp = models.DateTimeField(auto_now=True)

class UpdateDrug(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    timestamp = models.DateTimeField(auto_now=True)
