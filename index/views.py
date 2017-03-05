from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from account.models import ProfileInformation
from hnet.logger import CreateLogEntry


def index(request):
    profile_information = ProfileInformation.from_user(request.user)
    if profile_information is not None:
        account_type = profile_information.account_type

        if account_type == ProfileInformation.PATIENT:
            CreateLogEntry(request.user.username, "Patient logged in.")
            return redirect(reverse('index:patient'))
        elif account_type == ProfileInformation.DOCTOR:
            CreateLogEntry(request.user.username, "Doctor logged in.")
            return redirect(reverse('index:doctor'))
        elif account_type == ProfileInformation.NURSE:
            CreateLogEntry(request.user.username, "Nurse logged in.")
            return redirect(reverse('index:nurse'))
        elif account_type == ProfileInformation.ADMINISTRATOR:
            CreateLogEntry(request.user.username, "Administrator logged in.")
            return redirect(reverse('index:administrator'))
    else:
        return render(request, 'index/index.html')


def test_user_in_group(user, group_name):
    if user:
        return user.groups.filter(name=group_name)
    return False


# TODO: add group verification
@login_required
@user_passes_test(lambda u: test_user_in_group(u, 'Patient'))
def patient(request):
    CreateLogEntry(request.user.username, "Patient logged in.")
    return render(request, 'index/patient.html')


@login_required()
@user_passes_test(lambda u: test_user_in_group(u, 'Doctor'))
def doctor(request):
    CreateLogEntry(request.user.username, "Doctor logged in.")
    return render(request, 'index/doctor.html')


@login_required
@user_passes_test(lambda u: test_user_in_group(u, 'Nurse'))
def nurse(request):
    CreateLogEntry(request.user.username, "Nurse logged in.")
    return render(request, 'index/nurse.html')


@login_required
@user_passes_test(lambda u: test_user_in_group(u, 'Administrator'))
def administrator(request):
    CreateLogEntry(request.user.username, "Administrator logged in.")
    return render(request, 'index/administrator.html')
