import datetime
import math

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from reservation.models import Appointment
from reservation.forms import AppointmentFormForPatient, AppointmentFormForDoctor
from account.models import Patient, Doctor, ProfileInformation


@login_required
def calendar(request, month=timezone.now().month, year=timezone.now().year):
    days = calculate_day(str(month), str(year))

    month = int(month)
    year = int(year)

    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year


    month_name = datetime.date(1900, int(month), 1).strftime('%B')

    context = {'year': year, 'month_name': month_name,
               'prev_month': prev_month, 'prev_year': prev_year, 'next_month': next_month,
               'next_year': next_year, 'days': days}

    profile_information = ProfileInformation.from_user(request.user)
    if profile_information is not None:
        account_type = profile_information.account_type
        if account_type == ProfileInformation.PATIENT:
            appointments = request.user.patient.appointment_set.all()
            context['appointment_list'] = appointments
            return render(request, 'reservation/calendar.html', context)
        elif account_type == ProfileInformation.DOCTOR:
            appointments = request.user.doctor.appointment_set.all()
            context['appointment_list'] = appointments
            return render(request, 'reservation/calendar.html', context)

    return Http404()


def overview(request):
    single_appointment = Appointment.objects.all()[0]
    appointment = Appointment.objects.order_by('date_time').all()
    return render(request, 'reservation/overview.html',
                  {'appointment': appointment, 'single_appointment': single_appointment})


def detail(request, appointment_id):
    single_appointment = Appointment.objects.all()[0]
    appointment = Appointment.objects.order_by('date_time').all()
    return render(request, 'reservation/detail.html',
                  {'appointment': appointment, 'single_appointment': single_appointment})


@login_required
@permission_required('reservation.add_appointment')
def create_appointment(request):
    profile_information = ProfileInformation.from_user(request.user)

    if profile_information is None:
        raise PermissionDenied()

    account_type = profile_information.account_type
    if account_type == ProfileInformation.PATIENT:
        form_type = AppointmentFormForPatient
    elif account_type == ProfileInformation.DOCTOR:
        form_type = AppointmentFormForDoctor
    else:
        raise PermissionDenied()

    if request.method == 'POST':
        form = form_type(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect(reverse('reservation:create_done'))
    else:
        form = form_type()

    return render(request, 'reservation/appointment/create.html', {'form': form})


@login_required
@permission_required('reservation.add_appointment')
def create_appointment_done(request):
    return render(request, 'reservation/appointment/create_done.html')


@login_required
@permission_required('reservation.change_appointment')
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if not appointment.accessible_by_user(request.user):
        raise PermissionDenied()

    if request.method == 'POST':
        form = AppointmentFormForDoctor(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return render(request, 'reservation/appointment/edit.html', {'form': form, 'message': 'All changes saved.'})
    else:
        form = AppointmentFormForDoctor(instance=appointment)

    return render(request, 'reservation/appointment/edit.html', {'form': form})


@login_required
@permission_required('reservation.cancel_appointment')
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if not appointment.accessible_by_user(request.user):
        raise PermissionDenied()

    if request.method == 'POST':
        appointment.cancelled = True
        appointment.save()

        return render(request, 'reservation/appointment/delete_done.html')
    else:
        return render(request, 'reservation/appointment/delete.html', {'appointment': appointment})


def calculate_day(month, year):
    if(int(month) == 2 or int(month) == 1):
        year = int(year) - 1
        month = int(month) + 12

    final = 1 + (2*int(month)) + (3*(int(month) + 1)/5) + int(year) + math.floor(int(year)/4) - \
            math.floor(int(year)/100) + math.floor(int(year)/400) + 2

    remainder = math.floor(final/7)
    remainder *= 7
    final -= remainder

    thirtyone_months = ["12", "13", "3", "5", "7", "8", "10"]

    if((int(year)/4 and int(month) == 14) or (month == 14 and int(year)/100 and int(year)/400)):
        counter = 29
    if(month == 14):
        counter = 28
    elif(month in thirtyone_months or month == 13):
        counter = 31
    else:
        counter = 30

    count = 1
    days = []
    for i in range(0, int(final)):
        days.append("nothing")
    for i in range(int(final), counter + int(final)):
        days.append(count)
        count += 1

    return days