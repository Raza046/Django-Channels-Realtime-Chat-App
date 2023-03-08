from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your models here.
class Message(models.Model):

    room = models.ForeignKey("MessageRoom", related_name=("msg_room"), on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name=("Message_sender"), on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name=("Message_receiver"), on_delete=models.CASCADE)
    message = models.TextField()
    # Create a different model (Reaction) and then add foreign key there.
    # reaction = models.CharField(max_length=150, null=True)
    date = models.DateField(auto_now_add=True)

# create a reciever field here and then send the json data into the chat consumer. Then to the frontend.
# lets go

@receiver(post_save, sender=Message)
def MesageNotification(sender, instance, created, **kwargs):

    channel_layer = get_channel_layer()
    print(f"Sending notification to {instance.receiver.username}")
    sender_group_name = f"notif{instance.sender.id}"
    receiver_group_name = f"notif{instance.receiver.id}"
    async_function(sender_group_name, instance)
    async_function(receiver_group_name, instance)

    # print(f"Sending notification to {instance.receiver.username}")


def async_function(user_group, instance):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(

    user_group,{
        "type":"send_notification",
        "my_sender":instance.sender.username,
        "my_receiver":instance.receiver.username,
        "room":instance.room.group_name,
        "message":instance.message
    })

    print(f"Sending notification to {user_group}")



class MessageRoom(models.Model):

    group_name = models.CharField(max_length=150)
    first_user = models.ForeignKey(User, related_name=("first_user"), on_delete=models.CASCADE)
    second_user = models.ForeignKey(User, related_name=("second_user"), on_delete=models.CASCADE)
    # users_active = models.TextField()

    def __str__(self):
        return f'{self.first_user} -- {self.second_user}'

@receiver(post_save, sender=MessageRoom)
def CreateGroupName(sender, instance, created, **kwargs):
    if created:
        f_user = instance.first_user.username
        s_user = instance.second_user.username
        g_n = f"{f_user}_{s_user}_{instance.first_user.id}_{instance.second_user.id}"
        m_room = MessageRoom.objects.filter(id=instance.id).update(group_name=g_n)
