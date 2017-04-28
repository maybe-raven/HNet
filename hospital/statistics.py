from account.models import Patient


class Statistics():
    num_of_patients = 0
    avarage_visit_per_patient = 0
    avarage_leangth_of_stay = 0
    prescriptions_given = 0

    def __init__(self):
        self.num_of_patients = 0
        self.avarage_visit_per_patient = 0
        self.avarage_leangth_of_stay = 0
        self.prescriptions_given = 0

    def add_patient(self):
        self.num_of_patients += 1

    def add_prescription(self):
        self.prescriptions_given += 1

    def calculate_avarage_visit_per_patient(self):
        patients_list = Patient.objects.all()
        total_patients = patients_list[-1].id
