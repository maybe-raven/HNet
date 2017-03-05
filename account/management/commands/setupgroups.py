from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from account.models import Patient, ProfileInformation
from reservation.models import Appointment


class Command(BaseCommand):
    def handle(self, *args, **options):
        # If there are existing groups, there could be conflicts with the groups this script is about to create.
        # It is possible to merge them, but it would be too complicated and time-consuming to implement.
        # So just remove all of them.
        # Since we trust this script to create the groups properly,
        # we can always say 'y' to the prompt and let it handle the update of groups and permissions in the database.
        if Group.objects.count() > 0:
            while True:
                self.stdout.write(self.style.WARNING('You have existing groups in the database. '
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

        # Try to get all the permissions
        # This requires that the database has been migrated.
        # If not, then the permissions won't be found, and DoesNotExist error will be thrown.
        try:
            change_patient_permission = Permission.objects.get(codename='change_patient',
                                                               content_type=patient_content_type)
            change_profile_information_permission = Permission.objects.get(codename='change_profileinformation',
                                                                           content_type=profile_information_content_type)
            add_appointment_permission = Permission.objects.get(codename='add_appointment',
                                                                content_type=appointment_content_type)
            cancel_appointment_permission = Permission.objects.get(codename='cancel_appointment',
                                                                   content_type=appointment_content_type)
            change_appointment_permission = Permission.objects.get(codename='change_appointment',
                                                                   content_type=appointment_content_type)
        except Permission.DoesNotExist:
            raise CommandError('Required permissions not found. Did you forget to do database migration?')

        # Set up Patient group.
        patient_group = Group(name='Patient')
        patient_group.save()

        patient_group.permissions = [change_patient_permission, change_profile_information_permission,
                                     add_appointment_permission,
                                     cancel_appointment_permission, change_appointment_permission]
        patient_group.save()

        # Set up Doctor group.
        doctor_group = Group(name='Doctor')
        doctor_group.save()

        doctor_group.permissions = [change_profile_information_permission, add_appointment_permission,
                                    cancel_appointment_permission, change_appointment_permission]
        doctor_group.save()

        self.stdout.write(self.style.SUCCESS('Successfully set up all required groups.'))
