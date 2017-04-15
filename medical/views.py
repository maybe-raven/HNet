from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DrugForm, PrescriptionForm
from .models import Prescription
from hnet.logger import CreateLogEntry


@login_required
@permission_required('medical.add_drug')
def add_drug(request):
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'medical/drug/add_done.html')
    else:
        form = DrugForm()

    return render(request, 'medical/drug/add.html', {'form': form})


@login_required
@permission_required('medical.add_prescription')
def add_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            CreateLogEntry(request.user.username, "prescription added.")
            return render(request, 'medical/prescription/add_done.html')
    else:
        form = PrescriptionForm()

    return render(request, 'medical/prescription/add.html', {'form': form})


@login_required
@permission_required('medical.delete_prescription')
def remove_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)

    if request.method == 'POST':
        prescription.removed = True
        prescription.save()
        CreateLogEntry(request.user.username, "prescription removed.")

        return render(request, 'medical/prescription/remove_done.html')
    else:
        return render(request, 'medical/prescription.remove.html', {'prescription': prescription})
