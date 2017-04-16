from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import UserCreationForm, UserChangeForm, ProfileInformationForm, PatientCreationForm, PatientChangeForm, \
    AdministratorForm, DoctorCreationForm
from .models import ProfileInformation, Administrator, get_account_from_user
from hnet.logger import CreateLogEntry


def register_patient(request):
    if request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_information_form = ProfileInformationForm(request.POST)
        patient_form = PatientCreationForm(request.POST)

        if user_form.is_valid() and profile_information_form.is_valid() and patient_form.is_valid():
            user = user_form.save_as_patient_with_profile_information(patient_form, profile_information_form)

            auth.login(request, user)
            CreateLogEntry(request.user.username, "Patient account registered.")
            return render(request, 'account/patient/register_done.html')
    else:
        user_form = UserCreationForm()
        profile_information_form = ProfileInformationForm()
        patient_form = PatientCreationForm()

    return render(request, 'account/patient/register.html',
                  {'user_form': user_form, 'profile_information_form': profile_information_form,
                   'patient_form': patient_form})


@login_required
@permission_required('account.change_profileinformation')
@user_passes_test(lambda u: not u.is_superuser)
def profile(request):
    user = request.user
    profile_information = user.profile_information
    patient = user.patient

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        profile_information_form = ProfileInformationForm(request.POST, instance=profile_information)
        patient_form = PatientChangeForm(request.POST, instance=patient)
        if user_form.is_valid() and profile_information_form.is_valid() and patient_form.is_valid():
            user_form.save()
            profile_information_form.save()
            patient_form.save()
            CreateLogEntry(request.user.username, "Changed profile information.")
            return render(request, 'account/patient/profile.html',
                          {'profile_information_form': profile_information_form,
                           'user_form': user_form,
                           'patient_form': patient_form,
                           'message': 'All changes saved.'})
    else:
        user_form = UserChangeForm(instance=user)
        profile_information_form = ProfileInformationForm(instance=profile_information)
        patient_form = PatientChangeForm(instance=patient)

    return render(request, 'account/patient/profile.html',
                  {'profile_information_form': profile_information_form,
                   'patient_form': patient_form,
                   'user_form': user_form})


@login_required()
@permission_required('account.add_administrator')
@permission_required('account.add_profileinformation')
def create_administrator(request):
    creator = get_account_from_user(request.user)
    administrator_form = None

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_information_form = ProfileInformationForm(request.POST)

        if user_form.is_valid() and profile_information_form.is_valid():
            if isinstance(creator, Administrator):
                user_form.save_as_administrator_by_creator_with_profile_information(creator, profile_information_form)
                CreateLogEntry(request.user.username, "Administrator account registered.")
                return render(request, 'account/administrator/create_done.html')
            else:
                administrator_form = AdministratorForm(request.POST)
                if administrator_form.is_valid():
                    user_form.save_as_administrator_with_profile_information(administrator_form, profile_information_form)
                    CreateLogEntry(request.user.username, "Administrator account registered.")
                    return render(request, 'account/administrator/create_done.html')

    else:
        user_form = UserCreationForm()
        profile_information_form = ProfileInformationForm()
        if not isinstance(creator, Administrator):
            administrator_form = AdministratorForm()

    return render(request, 'account/administrator/create.html',
                  {'user_form': user_form,
                   'profile_information_form': profile_information_form,
                   'administrator_form': administrator_form})


@login_required()
@permission_required('account.add_doctor')
@permission_required('account.add_profileinformation')
def register_doctor(request):
    creator = get_account_from_user(request.user)
    doctor_form = None

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_information_form = ProfileInformationForm(request.POST)

        if user_form.is_valid() and profile_information_form.is_valid():
            if isinstance(creator, Administrator):
                user_form.save_as_doctor_by_creator_with_profile_information(creator, profile_information_form)
                CreateLogEntry(request.user.username, "Doctor account registered.")
                return render(request, 'account/doctor/register_done.html')
            else:
                doctor_form = DoctorCreationForm(request.POST)
                if doctor_form.is_valid():
                    user_form.save_as_doctor_with_profile_information(doctor_form, profile_information_form)
                    CreateLogEntry(request.user.username, "Doctor account registered.")
                    return render(request, 'account/doctor/register_done.html')
    else:
        user_form = UserCreationForm()
        profile_information_form = ProfileInformationForm()
        if not isinstance(creator, Administrator):
            doctor_form = DoctorCreationForm()

    return render(request, 'account/doctor/doctor.html',
                  {'user_form': user_form, 'profile_information_form': profile_information_form,
                   'doctor_form': doctor_form})


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
