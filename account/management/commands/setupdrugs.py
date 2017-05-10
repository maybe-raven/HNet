from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError
from django.db.models.deletion import ProtectedError
from django.contrib.auth.models import Group
from medical.models import Drug

default_password = '$teamname'


def check_table(model_type):
    return model_type.objects.count() > 0


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:

            if check_table(Drug):
                while True:
                    self.stdout.write(self.style.NOTICE('You have existing drugs. '
                                                        'Continuing will remove all of them and create new drugs. '
                                                        'Are you sure you want to continue? (y or n)'))

                    response = input()
                    if response == 'n':
                        print('No changes are made.')
                        return
                    elif response == 'y':
                        break

                Drug.objects.all().delete()

            Drug.objects.create(name="Insulin", description="lowers blood glucose levels").save()
            self.stdout.write(self.style.SUCCESS('Successfully created Insulin drug.'))

            Drug.objects.create(name="Morphine",
                                description="narcotic drug derived from opium, used to treat severe pain").save()
            self.stdout.write(self.style.SUCCESS('Successfully created Morphine drug.'))

            Drug.objects.create(name="Zithromycin", description="Azithromycin (Antibiotics)").save()
            self.stdout.write(self.style.SUCCESS('Successfully created Zithromycin drug.'))

        except OperationalError:
            raise CommandError('Operation cannot be completed. Did you forget to do database migration?')
        except ProtectedError:
            raise CommandError('Operation cannot be completed. Failed to remove existing records. '
                               'There\'re some records in the database referencing the existing records. '
                               'If you\'re sure you\'re OK with wiping the entire database, '
                               'try running `python manage.py flush`.')
