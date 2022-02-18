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
    problem = None
    if request.method == 'POST':
        data = UserCreationForm(request.POST)
        if data.is_valid():
            data.save()
        else:
            problem = 'Your registration was not valid, please try again'
    form = UserCreationForm()
    context = {
        'form': form,
        'problem': problem,
    }
    return render(request, 'thecode/register.html', context)

def loginpage(request):
    problem = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('searchpage')
        else:
            problem = 'Your login was incorrect, please try again'
    context = {
        'problem': problem
    }
    return render(request, 'thecode/login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('loginpage')

def searchpage(request):
    profiles = Profile.objects.all()
    exists = Profile.objects.filter(user=request.user).exists()
    print(exists)
    context = {
        'exists': exists,
        'profiles': profiles,
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
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm()
    if request.method == 'POST':
        print('post')
        if Profile.objects.filter(user=request.user).exists() == False:
            current = ProfileForm(request.POST)
        else:
            current = ProfileForm(request.POST, instance=profile)
        if current.is_valid():
            current = current.save(commit=False)
            current.user = request.user
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
    anyconversations = Conversation.objects.filter(participants=request.user).exists()
    print(anyconversations)
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
        conversation = Conversation.objects.filter(participants=sender).filter(participants=receiver).exists()
        if conversation == False:
            newconversation = Conversation()
            newconversation.save()
            newconversation.participants.add(sender)
            newconversation.participants.add(receiver)
            currentconversation = newconversation
        else:
            currentconversation = Conversation.objects.filter(participants=sender).filter(participants=receiver)
            currentconversation = currentconversation[0]
        record = Message(sender=sender, receiver=receiver, content=content, conversation=currentconversation, timestamp=timestamp)
        record.save()
        currentconversation.mostrecentmessage = record
        currentconversation.save()
        return redirect('messagespage')
    return render(request, 'thecode/writemessage.html', context)

def conversationpage(request, id):
    conversation = Conversation.objects.get(id=id)
    if conversation.participants.all()[0] == request.user:
        exchangeperson = conversation.participants.all()[1]
    else:
        exchangeperson = conversation.participants.all()[0]
    messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
    profile = Profile.objects.get(user=exchangeperson)
    idnumber = profile.id
    context = {
        'messages': messages,
        'exchangeperson': exchangeperson,
        'idnumber': idnumber,
    }
    return render(request, 'thecode/conversation.html', context)

def searchwritemessage(request, id):
    profile = Profile.objects.get(id=id)
    if Conversation.objects.filter(participants=request.user).filter(participants=profile.user).exists():
        conversation = Conversation.objects.filter(participants=request.user).filter(participants=profile.user)
        conversation = conversation[0]
        messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
    else:
        messages = None
    context = {
        'profile': profile,
        'messages': messages,
    }
    if request.method == 'POST':
        sender = request.user
        receiver = profile.user
        content = request.POST['content']
        timestamp = datetime.now()
        conversation = Conversation.objects.filter(participants=sender).filter(participants=receiver).exists()
        if conversation == False:
            newconversation = Conversation()
            newconversation.save()
            newconversation.participants.add(sender)
            newconversation.participants.add(receiver)
            currentconversation = newconversation
        else:
            currentconversation = Conversation.objects.filter(participants=sender).filter(participants=receiver)
        record = Message(sender=sender, receiver=receiver, content=content, conversation=currentconversation[0], timestamp=timestamp)
        record.save()
        currentconversation.mostrecentmessage = record
        currentconversation.save()
        return redirect('messagespage')
    return render(request, 'thecode/writemessage.html', context)
