from django.db import models
from hospital.models import Hospital, TreatmentSession
from account.models import Doctor, Patient
from hnet.logger import CreateLogEntry


class DiagnosisCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Diagnosis(models.Model):
    treatment_session = models.ForeignKey(TreatmentSession, on_delete=models.CASCADE, null=True)

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)
    """A high level summary of this patient's condition, including any useful, medical information for the treatment"""
    summary = models.TextField(blank=True)
    category = models.ManyToManyField(DiagnosisCategory, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def get_patient(self):
        if self.patient:
            return self.patient

        return self.treatment_session.patient

    def __str__(self):
        if self.summary:
            return self.summary.split('\n')[0][:80]
        else:
            return "Diagnosis created at %s" % self.creation_timestamp.ctime()

    class Meta:
        permissions = (
            ('view_diagnosis', 'Can view diagnoses'),
        )


class Test(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.PROTECT)

    description = models.TextField()
    results = models.TextField()
    notes = models.TextField()
    released = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('request_test', 'Can request tests'),
            ('upload_test_results', 'Can upload test results')
        )


class Drug(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('remove_drug', 'Can remove drugs'),
            ('view_drug', 'Can view drugs'),
        )


class Prescription(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    instruction = models.TextField()

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('view_prescription', 'Can view prescriptions'),
        )
