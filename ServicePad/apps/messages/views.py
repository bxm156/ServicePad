# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from models import Message
from forms import ComposeMessageForm
from django.contrib.auth.decorators import login_required

@login_required
def inbox(request):
    messages = Message.objects.filter(toUser=request.user)
    return render(request, 'list_messages.djhtml', 
                            { 'messages': messages})

def message(request, message_id):
    sentMessage = get_object_or_404(Message, pk=message_id, toUser=request.user)
    subject = sentMessage.subject
    date_sent = sentMessage.date_sent
    message = sentMessage.message
    fromUser = sentMessage.fromUser
    toUser = sentMessage.toUser
    
    context = {
        "from" : fromUser,
        "to" : toUser,
        "subject" : subject,
        "date_sent" : date_sent,
        'message' : message
               }
    
    return render(request, 'view_message.djhtml', context)

def compose(request):
    if request.POST:
        new_data = request.POST.copy()
        message = Message(fromUser=request.user)
        message_form = ComposeMessageForm(new_data,instance=message)
        if message_form.is_valid():
            #Create the message and save the values to it
            message_form.save()
            return redirect("/account/messages/")
    else:
        message_form = ComposeMessageForm()
    return render(request,'compose_message.djhtml',
                                {'form':message_form})
    
    
    

