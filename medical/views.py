from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
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

def update_drug(request)
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'medical/drug/update_done.html')
    else:
        form = DrugForm()

    return render(request, 'medical/drug/update.html',{'form':form})
