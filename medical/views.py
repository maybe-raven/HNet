from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from medical.models import Drug
from hnet.logger import CreateLogEntry
from .forms import DrugForm


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
@permission_required('medical.remove_drug')
@user_passes_test(lambda u: not u.is_superuser)
def remove_drug(request, drug_id):
    drug = get_object_or_404(Drug, pk=drug_id)

    if not drug.active:
        return render(request, 'medical/drug/already_removed.html')

    if request.method == 'POST':
        drug.active = False
        drug.save()
        CreateLogEntry(request.user.username, "Drug removed.")
        return render(request, 'medical/drug/remove_done.html')
    else:
        return render(request, 'medical/drug/remove.html', {'drug': drug})
