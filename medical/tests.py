from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user
from django.core.urlresolvers import reverse
from hospital.models import Hospital
from account.models import Patient, create_default_account



