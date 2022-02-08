from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    skillstolearn = models.CharField(max_length=200)
    skillstoteach = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.user.username

class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    
    def __str__(self):
        return str(self.participants.all()[0]) + ' and ' + str(self.participants.all()[1])

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    conversation = models.ForeignKey(Conversation, default=None, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.sender.username + ' to ' + self.receiver.username
