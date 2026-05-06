"""Student 3 - Prasiddha Pant"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages as flash_messages
from .models import Message
from teams.models import Team
from core.models import AuditLog


# Create your views here.

@login_required
def inbox(request): 
    msgs = Message.objects.filter(recipient = request.user, status = 'SENT')
    unread = msgs.filter(is_read = False).count()
    return render(request, 'messaging/inbox.html', {'msgs': msgs, 'unread': unread, 'active': 'inbox'})

@login_required
def sent(request):
    msgs = Message.objects.filter(sender = request.user, status = 'SENT')
    return render(request, 'messaging/inbox.html', {'msgs': msgs, 'active': 'sent'})

@login_required
def drafts(request): 
    msgs = Message.objects.filter(sender = request.user, status = 'DRAFT')
    return render(request, 'messaging/inbox.html', {'msgs': msgs, 'active': 'draft'})

@login_required
def message_detail(request, pk):
    msg = get_object_or_404(Message, pk = pk)
    if msg.recipient == request.user and not msg.is_read: 
        msg.is_read = True
        msg.save()
    return render(request, 'messaging/message_detail.html', {'msg': msg})

@login_required
def compose(request): 
    users = User.objects.exclude(pk = request.user.pk)
    teams = Team.objects.all()

    if request.method == 'POST': 
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()
        recipient_id = request.POST.get('recipient')
        recipient_team_id = request.POST.get('recipient_team')
        action = request.POST.get('action', 'send')

        if not subject or not body: 
            flash_messages.error(request, 'Subject and message body are required.')
            return render(request, 'messaging/compose.html', {'users': users, 'teams': teams})
        
        msg = Message(
            sender = request.user, subject = subject, body = body, 
            status = 'DRAFT' if action == 'draft' else 'SENT'
        )

        if recipient_id: 
            msg.recipient_id = recipient_id
        if recipient_team_id: 
            msg.recipient_team_id = recipient_team_id
        msg.save()

        AuditLog.objects.create(user = request.user, action = 'CREATE', 
                                entity_type = 'Message', entity_id = msg.pk)
        if action == 'draft': 
            flash_messages.success(request, 'Message saved as draft.')
            return redirect('messaging:drafts')
        else:
            flash_messages.success(request, 'Message sent successfully.')
            return redirect('messaging:sent')
        
    return render(request, 'messaging/compose.html', {'users': users, 'teams': teams})