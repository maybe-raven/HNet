from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from hospital.models import TreatmentSession
from hnet.logger import CreateLogEntry


@login_required
@permission_required('hospital.change_treatmentsession')
@user_passes_test(lambda u: not u.is_superuser)
def discharge_patient(request, treatmentsession_id):
    session = get_object_or_404(TreatmentSession, pk=treatmentsession_id)

    if session.discharge_timestamp is not None:
        return render(request, 'discharge/already_discharged.html')

    if request.method == 'POST':
        session.discharge_timestamp = datetime.now()
        session.save()
        CreateLogEntry(request.user.username, "Patient discharged.")
        return render(request, 'discharge/discharge_done.html')
    else:
        return render(request, 'discharge/discharge.html', {'session': session})


def logView(request):
    return render(request, 'hospital/viewlog.html')
