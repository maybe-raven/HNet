import datetime

from django import forms
from django.db.models import Q
from reservation.models import Appointment


class BaseAppointmentForm(forms.ModelForm):
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.datetime.now().date():
            raise forms.ValidationError('Cannot schedule appointment with a past date.')

        return date

    def clean(self):
        """
        This validates that the provided appointment time does not conflict with another already existing appointment.
        """
        cleaned_data = super(BaseAppointmentForm, self).clean()

        # Make sure the data required for this validation process are valid,
        # otherwise don't even bother running this validation
        if 'date' not in cleaned_data or 'start_time' not in cleaned_data or 'end_time' not in cleaned_data:
            return cleaned_data

        # Get the valid date/time data
        date = cleaned_data['date']
        start_time = cleaned_data['start_time']
        end_time = cleaned_data['end_time']

        # Construct a query to find the appointments that have time conflicts with this one
        cancelled_q = Q(cancelled=False)
        date_q = Q(date=date)
        start_time_q = Q(start_time__lte=start_time) & Q(end_time__gte=start_time)
        end_time_q = Q(start_time__lte=end_time) & Q(start_time__gte=end_time)
        overall_time = Q(start_time__gte=start_time) & Q(start_time__lte=end_time)
        time_q = start_time_q | end_time_q | overall_time
        q = cancelled_q & date_q & time_q
        # Exclude this record from the results, since an appointment cannot conflict with itself.
        if self.instance.id is not None:
            q = ~Q(pk=self.instance.id) & q

        # Count the number of results returned from the query and determine if a conflict exists.
        if Appointment.objects.filter(q).count() > 0:
            raise forms.ValidationError('The time slot is not available, please try a different one.')

        return cleaned_data

    class Meta:
        model = Appointment
        fields = ['title', 'location', 'date', 'start_time', 'end_time']


class AppointmentFormForPatient(BaseAppointmentForm):
    def save(self, creator=None, commit=True):
        if creator is not None:
            appointment = super(AppointmentFormForPatient, self).save(commit=False)
            appointment.patient = creator.patient

            if commit:
                appointment.save()
        else:
            appointment = super(AppointmentFormForPatient, self).save(commit)

        return appointment

    class Meta:
        model = Appointment
        fields = BaseAppointmentForm.Meta.fields + ['doctor']


class AppointmentFormForDoctor(BaseAppointmentForm):
    def save(self, creator=None, commit=True):
        if creator is not None:
            appointment = super(AppointmentFormForDoctor, self).save(commit=False)
            appointment.doctor = creator.doctor

            if commit:
                appointment.save()
        else:
            appointment = super(AppointmentFormForDoctor, self).save(commit)

        return appointment

    class Meta:
        model = Appointment
        fields = BaseAppointmentForm.Meta.fields + ['patient']
