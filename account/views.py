from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserCreationForm, UserChangeForm, ProfileInformationForm, PatientCreationForm, PatientChangeForm
from .models import ProfileInformation
from hnet.logger import CreateLogEntry


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_information_form = ProfileInformationForm(request.POST)
        patient_form = PatientCreationForm(request.POST)

        if user_form.is_valid() and profile_information_form.is_valid() and patient_form.is_valid():
            user = user_form.save_as_patient_with_profile_information(patient_form, profile_information_form)

            auth.login(request, user)
            CreateLogEntry(request.user.username, "Patient account registered.")
            return redirect(reverse('account:register_done'))
    else:
        user_form = UserCreationForm()
        profile_information_form = ProfileInformationForm()
        patient_form = PatientCreationForm()

    return render(request, 'account/register.html',
                  {'user_form': user_form, 'profile_information_form': profile_information_form,
                   'patient_form': patient_form})


def register_done(request):
    return render(request, 'account/register_done.html')


@login_required
@permission_required('account.change_profileinformation')
def profile(request):
    profile_information = ProfileInformation.from_user(request.user)
    if profile_information is None or profile_information.account_type != ProfileInformation.PATIENT:
        raise PermissionDenied()

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_information_form = ProfileInformationForm(request.POST, instance=profile_information)
        if profile_information_form.is_valid():
            profile_information_form.save()
            CreateLogEntry(request.user.username, "Changed profile information.")
            return render(request, 'account/profile.html', {'profile_information_form': profile_information_form, 'user_form': user_form, 'message': 'All changes saved.'})
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_information_form = ProfileInformationForm(instance=profile_information)

    return render(request, 'account/profile.html', {'profile_information_form': profile_information_form, 'user_form': user_form})


@login_required
@permission_required('account.change_patient')
def patient(request):
    profile_information = ProfileInformation.from_user(request.user)
    if profile_information is None or profile_information.account_type != ProfileInformation.PATIENT:
        raise PermissionDenied()

    if request.method == 'POST':
        form = PatientChangeForm(request.POST, instance=request.user.patient)
        if form.is_valid():
            form.save()
            CreateLogEntry(request.user.username, "Changed medical information.")
            return render(request, 'account/patient.html', {'form': form, 'message': 'All changes saved.'})
    else:
        form = PatientChangeForm(instance=request.user.patient)

    return render(request, 'account/patient.html', {'form': form})


@login_required()
@permission_required('account.add_administrator', 'account.add_profileinformation')
def administrators(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_information_form = ProfileInformationForm(request.POST)
        if user_form.is_valid() and profile_information_form.is_valid():
            user = user_form.save_as_administrator_with_profile_information(user_form, profile_information_form)

            auth.login(request, user)
            CreateLogEntry(request.user.username, "Administrator account registered.")
            return redirect(reverse('account:register_done'))
    else:
        user_form = UserCreationForm()
        profile_information_form = ProfileInformationForm()

    return render(request, 'account/register.html',
                  {'user_form': user_form, 'profile_information_form': profile_information_form})


@login_required()
@permission_required('account.add_doctor', 'account.add_profileinformation')
def doctor(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_information_form = ProfileInformationForm(request.POST)
        if user_form.is_valid() and profile_information_form.is_valid():
            user = user_form.save_as_doctor_with_profile_information(user_form, profile_information_form)

            auth.login(request, user)
            CreateLogEntry(request.user.username, "Doctor account registered.")
            return redirect(reverse('account:register_done'))
        else:
            user_form = UserCreationForm()
            profile_information_form = ProfileInformationForm()

        return render(request, 'account/administrator.html',
                      {'user_form': user_form, 'profile_information_form': profile_information_form})


@login_required()
@permission_required('account.add_nurse', 'account.add_profileinformation')
def nurse(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_information_form = ProfileInformationForm(request.POST)
        if user_form.is_valid() and profile_information_form.is_valid():
            user = user_form.save_as_nurse_with_profile_information(user_form, profile_information_form)

            auth.login(request, user)
            CreateLogEntry(request.user.username, "Nurse account registered.")
            return redirect(reverse('account:register_done'))
        else:
            user_form = UserCreationForm()
            profile_information_form = ProfileInformationForm()

        return render(request, 'account/register.html',
                      {'user_form': user_form, 'profile_information_form': profile_information_form})
