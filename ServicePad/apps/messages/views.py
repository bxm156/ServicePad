# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from models import Message
from forms import ComposeMessageForm
from django.contrib.auth.decorators import login_required

@login_required
def inbox(request):
    
    #Get all the messages for a user
    """
    SELECT `messages_message`.`id`, `messages_message`.`toUser_id`, `messages_message`.`fromUser_id`,
    `messages_message`.`subject`, `messages_message`.`message`, `messages_message`.`date_sent` 
    FROM `messages_message` WHERE `messages_message`.`toUser_id` = 6 
    """
    messages = Message.objects.filter(toUser=request.user)
    print messages.query.__str__()
    
    return render(request, 'list_messages.djhtml', 
                            { 'messages': messages})

def message(request, message_id):
    #Gets a message object
    """
    SELECT * FROM `messages_message` WHERE `messages_message`.`toUser_id` = 6 AND `messages_message`.`id` = 1
    """
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
        to = request.GET.get('to',None)
        msg = Message(toUser_id=to)
        message_form = ComposeMessageForm(instance=msg)
    return render(request,'compose_message.djhtml',
                                {'form':message_form})
    
    
    

