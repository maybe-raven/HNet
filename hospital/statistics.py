class Statistics():
    num_of_patients = 0
    avarage_visit_per_patient = 0
    avarage_leangth_of_stay = 0
    prescriptions_given = 0
    display = ""

    def __init__(self):
        self.num_of_patients = 0
        self.avarage_visit_per_patient = 0
        self.avarage_leangth_of_stay = 0
        self.prescriptions_given = 0
        self.display = ""

    def add_patient(self):
        self.num_of_patients += 1

    def add_prescription(self):
        self.prescriptions_given += 1

    def calculate_avarage_visit_per_patient(self):
        from account.models import Patient
        total_patients = Patient.objects.last().id
        self.avarage_visit_per_patient = self.num_of_patients / total_patients

    def to_string(self):
        stat_file
        self.display += "Number of patients visiting the hospital : " + str(self.num_of_patients) + "\n"
        self.display += "Avarage visits per patient : " + str(self.avarage_visit_per_patient) + "\n"
        self.display += "Avarage length of stay : " + str(self.avarage_leangth_of_stay) + "\n"
        self.display += "Number of prescriptions given : " + str(self.prescriptions_given) + "\n"