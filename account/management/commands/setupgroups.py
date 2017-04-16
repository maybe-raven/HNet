from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.utils import OperationalError
from account.models import Patient, ProfileInformation, Administrator, Doctor, Nurse
from medical.models import Drug, Prescription
from account.models import Patient, ProfileInformation, Administrator, Doctor
from medical.models import Drug, Diagnosis, Test
from hospital.models import TreatmentSession
from reservation.models import Appointment


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            # If there are existing groups, there could be conflicts with the groups this script is about to create.
            # It is possible to merge them, but it would be too complicated and time-consuming to implement.
            # So just remove all of them.
            # Since we trust this script to create the groups properly,
            # we can always say 'y' to the prompt and let it handle the update of groups and permissions in the database
            if Group.objects.count() > 0:
                while True:
                    self.stdout.write(self.style.NOTICE('You have existing groups in the database. '
                                                        'Continuing will remove all of them, '
                                                        'and create and set up only those required by the application.\n'
                                                        'Are you sure you want to continue? (y or n)'))

                    response = input()
                    if response == 'n':
                        print('No changes are made.')
                        return
                    elif response == 'y':
                        break

                Group.objects.all().delete()

            # Get all the content types
            # As long as the model classes (python code) are in the project, this won't throw any error.
            patient_content_type = ContentType.objects.get_for_model(Patient)
            profile_information_content_type = ContentType.objects.get_for_model(ProfileInformation)
            appointment_content_type = ContentType.objects.get_for_model(Appointment)
            administrator_content_type = ContentType.objects.get_for_model(Administrator)
            doctor_content_type = ContentType.objects.get_for_model(Doctor)
            drug_content_type = ContentType.objects.get_for_model(Drug)
            prescription_content_type = ContentType.objects.get_for_model(Prescription)
            treatment_session_content_type = ContentType.objects.get_for_model(TreatmentSession)
            diagnosis_content_type = ContentType.objects.get_for_model(Diagnosis)
            treatment_session_content_type = ContentType.objects.get_for_model(TreatmentSession)
            test_content_type = ContentType.objects.get_for_model(Test)

            # Try to get all the permissions
            # This requires that the database has been migrated.
            # If not, then the permissions won't be found, and DoesNotExist error will be thrown.
            change_patient_permission = Permission.objects.get(codename='change_patient',
                                                               content_type=patient_content_type)
            change_profile_information_permission = Permission.objects.get(codename='change_profileinformation',
                                                                           content_type=profile_information_content_type)
            add_profile_information_permission = Permission.objects.get(codename='add_profileinformation',
                                                                        content_type=profile_information_content_type)
            add_appointment_permission = Permission.objects.get(codename='add_appointment',
                                                                content_type=appointment_content_type)
            cancel_appointment_permission = Permission.objects.get(codename='cancel_appointment',
                                                                   content_type=appointment_content_type)
            change_appointment_permission = Permission.objects.get(codename='change_appointment',
                                                                   content_type=appointment_content_type)
            view_appointment_permission = Permission.objects.get(codename='view_appointment',
                                                                 content_type=appointment_content_type)
            add_administrator_permission = Permission.objects.get(codename='add_administrator',
                                                                  content_type=administrator_content_type)
            add_doctor_permission = Permission.objects.get(codename='add_doctor',
                                                           content_type=doctor_content_type)
            add_drug_permission = Permission.objects.get(codename='add_drug',
                                                         content_type=drug_content_type)
            view_prescription_permission = Permission.objects.get(codename='view_prescription',
                                                                  content_type=prescription_content_type)
            view_patients_permission = Permission.objects.get(codename='view_patients',
                                                              content_type=patient_content_type)
            discharge_patient_permission = Permission.objects.get(codename='discharge_patient',
                                                                  content_type=treatment_session_content_type)
            add_diagnosis_permission = Permission.objects.get(codename='add_diagnosis',
                                                              content_type=diagnosis_content_type)
            change_diagnosis_permission = Permission.objects.get(codename='change_diagnosis',
                                                                 content_type=diagnosis_content_type)
            remove_drug_permission = Permission.objects.get(codename='remove_drug',
                                                            content_type=drug_content_type)
            view_diagnosis_permission = Permission.objects.get(codename='view_diagnosis',
                                                               content_type=diagnosis_content_type)
            view_treatment_session_permission = Permission.objects.get(codename='view_treatmentsession',
                                                                       content_type=treatment_session_content_type)
            request_test_permission = Permission.objects.get(codename='request_test',
                                                             content_type=test_content_type)
            upload_test_results_permission = Permission.objects.get(codename='upload_test_results',
                                                                    content_type=test_content_type)
            view_drug_permission = Permission.objects.get(codename='view_drug',
                                                          content_type=drug_content_type)
        except (Permission.DoesNotExist, OperationalError):
            raise CommandError('Operation cannot be completed. Did you forget to do database migration?')

        # Set up Patient group.
        patient_group = Group(name='Patient')
        patient_group.save()

        patient_group.permissions = [change_patient_permission, change_profile_information_permission,
                                     add_appointment_permission,
                                     cancel_appointment_permission, change_appointment_permission,
                                     view_appointment_permission, view_prescription_permission]
        patient_group.save()

        # Set up Nurse group.
        nurse_group = Group(name='Nurse')
        nurse_group.save()

        nurse_group.permissions = [view_prescription_permission, view_patients_permission]
        nurse_group.save()

        # Set up Doctor group.
        doctor_group = Group(name='Doctor')
        doctor_group.save()

        doctor_group.permissions = [change_profile_information_permission, add_appointment_permission,
                                    cancel_appointment_permission, change_appointment_permission,
                                    view_appointment_permission, add_diagnosis_permission,
                                    change_diagnosis_permission, request_test_permission,
                                    upload_test_results_permission, discharge_patient_permission,
                                    view_diagnosis_permission, view_treatment_session_permission,
                                    view_patients_permission, view_prescription_permission]
        doctor_group.save()

        # Set up Nurse group.
        nurse_group = Group(name='Nurse')
        nurse_group.save()

        nurse_group.permissions = [view_diagnosis_permission, view_treatment_session_permission]
        nurse_group.save()

        # Set up Administrator group
        administrator_group = Group(name='Administrator')
        administrator_group.save()

        administrator_group.permissions = [add_administrator_permission, add_doctor_permission,
                                           add_profile_information_permission, add_drug_permission,
                                           remove_drug_permission, view_drug_permission]
        administrator_group.save()

        self.stdout.write(self.style.SUCCESS('Successfully set up all required groups.'))
