from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q

# Create your views here.
@login_required
def index(request):
    template_data = {}
    template_data['title'] = 'HireMap - Messages'
    template_data['sidebar_messages'] = sidebar_messages(request)
    if request.method == 'GET':
        search = request.GET.get('search')
        if search:
            template_data['sidebar_messages'] = sidebar_messages(request, search)
        other_user_id = request.GET.get('other_user_id') # still tentative if id or username should be used
        if other_user_id:
            messages = Message.objects.filter(
                    (Q(sender=request.user) & Q(recipient__id=other_user_id)) |
                    (Q(sender__id=other_user_id) & Q(recipient=request.user))
                ).order_by('timestamp')
            try:
                template_data['other_user'] = User.objects.get(id=other_user_id)
                template_data['messages'] = messages
            except User.DoesNotExist:
                template_data['error'] = 'User not found'
    if request.method == 'POST':
        other_user_id = request.POST.get('other_user_id')
        if other_user_id:
            success = create_message(request, other_user_id)
            if success:
                template_data['other_user'] = User.objects.get(id=other_user_id)
                template_data['messages'] = Message.objects.filter(
                    (Q(sender=request.user) & Q(recipient__id=other_user_id)) |
                    (Q(sender__id=other_user_id) & Q(recipient=request.user))
                ).order_by('timestamp')
            else:
                template_data['error'] = 'Failed to send message'
    return render(request, 'messages/index.html', {'template_data': template_data})

@login_required
def create_message(request, recipient_id):
    content = request.POST.get('content')
    if recipient_id and content:
        try:
            recipient = User.objects.get(id=recipient_id)
            message = Message.objects.create(sender=request.user, recipient=recipient, content=content)
            message.save()
            return True
        except User.DoesNotExist:
            return False
    return False

@login_required
def sidebar_messages(request, search_term=None):
    sidebar_messages_info = []
    if hasattr(request.user, 'applicant'):
        sidebar_messages = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).order_by('-timestamp')
        if search_term:
            sidebar_messages = sidebar_messages.filter(
                Q(sender__recruiter__company__icontains=search_term) | 
                Q(sender__recruiter__first_name__icontains=search_term) |
                Q(sender__recruiter__last_name__icontains=search_term)
            )
    elif hasattr(request.user, 'recruiter'):
        sidebar_messages = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).order_by('-timestamp')
        if search_term:
            sidebar_messages = sidebar_messages.filter(
                Q(sender__applicant__first_name__icontains=search_term) |
                Q(sender__applicant__last_name__icontains=search_term)
            )
    else:
        # User doesn't have applicant or recruiter profile
        sidebar_messages = Message.objects.none()
    unique_pairs = set()
    deduped_messages = []
    for msg in sidebar_messages:
        pair = tuple(sorted([msg.sender.id, msg.recipient.id]))
        if pair not in unique_pairs:
            unique_pairs.add(pair)
            deduped_messages.append(msg)
    for msg in deduped_messages:
        if msg.sender == request.user:
            other_user = msg.recipient
        else:
            other_user = msg.sender
        if hasattr(other_user, 'applicant'):
            first_name = other_user.applicant.first_name
            last_name = other_user.applicant.last_name
            company = ''
        elif hasattr(other_user, 'recruiter'):
            first_name = other_user.recruiter.first_name
            last_name = other_user.recruiter.last_name
            company = other_user.recruiter.company_name
        sidebar_messages_info.append({
            'user_id': other_user.id,
            'first_name': first_name,
            'last_name': last_name,
            'company': company,
            'last_message': msg.content,
            'timestamp': msg.timestamp,
        })
    return sidebar_messages_info