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

    def read_file(self):
        stat_file = open('hospital/statistics.txt', 'r')
        nums = []
        for line in stat_file:
            nums.append(int(line.strip()))

        self.num_of_patients = nums[0]
        self.avarage_visit_per_patient = nums[1]
        self.avarage_leangth_of_stay = nums[2]
        self.prescriptions_given = nums[3]

    def write_file(self):
        stat_file = open('hospital/statistics.txt', 'w')
        stat_file.write(str(self.num_of_patients) + "\n")
        stat_file.write(str(self.avarage_visit_per_patient) + "\n")
        stat_file.write(str(self.avarage_leangth_of_stay) + "\n")
        stat_file.write(str(self.prescriptions_given) + "\n")



    def add_patient(self):
        self.num_of_patients += 1

    def add_prescription(self):
        self.prescriptions_given += 1

    def calculate_avarage_visit_per_patient(self):
        from account.models import Patient
        total_patients = Patient.objects.last().id
        self.avarage_visit_per_patient = self.num_of_patients / total_patients

    def to_string(self):
        self.read_file(self)
        self.display += "Number of patients visiting the hospital : " + str(self.num_of_patients) + "\n"
        self.display += "Avarage visits per patient : " + str(self.avarage_visit_per_patient) + "\n"
        self.display += "Avarage length of stay : " + str(self.avarage_leangth_of_stay) + "\n"
        self.display += "Number of prescriptions given : " + str(self.prescriptions_given) + "\n"