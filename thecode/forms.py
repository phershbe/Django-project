from django.forms import ModelForm
from .models import Profile, Message

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
