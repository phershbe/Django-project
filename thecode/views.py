from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ProfileForm, MessageForm
from .models import Profile, Message, Conversation
from datetime import datetime

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('searchpage')
    return render(request, 'thecode/index.html')

def registerpage(request):
    if request.method == 'POST':
        data = UserCreationForm(request.POST)
        if data.is_valid():
            data.save()
    form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'thecode/register.html', context)

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('searchpage')
    return render(request, 'thecode/login.html')

def logoutuser(request):
    logout(request)
    return redirect('loginpage')

def searchpage(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'thecode/search.html', context)

def profilecreate(request):
    if request.method == 'POST':
        profile = ProfileForm(request.POST)
        if profile.is_valid():
            profile.save()
        return redirect('searchpage')
    form = ProfileForm()
    context = {
        'form': form
    }
    return render(request, 'thecode/profile.html', context)

def profileupdate(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        print('post')
        current = ProfileForm(request.POST, instance=profile)
        if current.is_valid():
            print('is valid')
            current.save()
        else:
            print('is not valid')
            print(current.errors.as_data())
        return redirect('searchpage')
    
    context = {
        'form': form
    }
    return render(request, 'thecode/profileupdate.html', context)

def messagespage(request):
    conversations = Conversation.objects.filter(participants=request.user)
    context = {
        'conversations': conversations,
    }
    return render(request, 'thecode/messages.html', context)

def writemessage(request, id):
    profile = Profile.objects.get(id=id)
    context = {
        'profile': profile,
    }
    if request.method == 'POST':
        sender = request.user
        receiver = profile.user
        content = request.POST['content']
        timestamp = datetime.now()
        print(sender, receiver, content, timestamp)
        record = Message(sender=sender, receiver=receiver, content=content, timestamp=timestamp)
        record.save()
        senderprofile = Profile.objects.get(user=sender)
        receiverprofile = Profile.objects.get(user=receiver)
        record.conversation.add(senderprofile)
        record.conversation.add(receiverprofile)
        print(senderprofile, receiverprofile)
        return redirect('messagespage')
    return render(request, 'thecode/writemessage.html', context)

def conversationpage(request, id):
    conversation = Conversation.objects.get(id=id)
    if conversation.participants.all()[0] == request.user:
        exchangeperson = conversation.participants.all()[1]
    else:
        exchangeperson = conversation.participants.all()[0]
    messages = Message.objects.filter(conversation=conversation)
    profile = Profile.objects.get(user=exchangeperson)
    idnumber = profile.id
    context = {
        'messages': messages,
        'exchangeperson': exchangeperson,
        'idnumber': idnumber,
    }
    return render(request, 'thecode/conversation.html', context)
