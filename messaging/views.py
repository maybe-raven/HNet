from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from .models import Message

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        form.sender = request.user
        if form.is_valid():
            form.save()
            return render(request, 'messaging/send_done.html')
    else:
        form = MessageForm()

    return render(request, 'messaging/send.html', {'form': form})

@login_required
def view_message(request):
    if request.method == 'POST':
        message = MessageForm(request.POST)
        m = Message(message)
        content = m.content
        content.seen = True
        message.save()
    else:
        form = MessageForm()

    return render(request, 'messaging/view.html', {'form':form})
