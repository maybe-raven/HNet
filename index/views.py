from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from account.models import ProfileInformation
from hnet.logger import CreateLogEntry
from .forms import StephenLoginForm
from hnet.logger import readLog



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


def test_user_account_type(user, account_type):
    """
    Test whether or not the given user is the given account type.
    """

    profile_information = ProfileInformation.from_user(user)
    if profile_information is not None:
        return profile_information.account_type == account_type
    return False


def log(request):
    log = readLog()
    return render(request, 'hospital/viewlog.html', {"log": log})


# TODO: add group verification
@login_required
@user_passes_test(lambda u: test_user_account_type(u, ProfileInformation.PATIENT))
def patient(request):
    CreateLogEntry(request.user.username, "Patient logged in.")
    return render(request, 'index/patient.html')


@login_required()
@user_passes_test(lambda u: test_user_account_type(u, ProfileInformation.DOCTOR))
def doctor(request):
    CreateLogEntry(request.user.username, "Doctor logged in.")
    return render(request, 'index/administrator.html')


@login_required
@user_passes_test(lambda u: test_user_account_type(u, ProfileInformation.NURSE))
def nurse(request):
    CreateLogEntry(request.user.username, "Nurse logged in.")
    return render(request, 'index/administrator.html')


@login_required
@user_passes_test(lambda u: test_user_account_type(u, ProfileInformation.ADMINISTRATOR))
def administrator(request):
    CreateLogEntry(request.user.username, "Administrator logged in.")
    return render(request, 'index/administrator.html')


def stephen(request):
    if request.method == 'POST':
        form = StephenLoginForm(request.POST)
        if form.is_valid():
            return render(request, 'index/stephen.html')
    else:
        form = StephenLoginForm()
    return render(request, 'index/stephen_login.html', {'form': form})
