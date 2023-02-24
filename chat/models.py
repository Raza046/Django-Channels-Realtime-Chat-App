from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.urls import reverse
from django.db.models import Q

# class CommonFields(models.Model):
#     message = models.TextField()

#     class Meta:
#         abstract = True


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prof_image = models.FileField(upload_to="static")
    friends = models.ManyToManyField("UserProfile", related_name=("user_friends"), blank=True)
    block_users = models.ManyToManyField("UserProfile", related_name=("blocked_users"), blank=True)
    address = models.TextField()
    city = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name = ("UserProfile")
        verbose_name_plural = ("UserProfiles")
        # unique_together = ['user', 'friends']

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("UserProfile_detail", kwargs={"pk": self.pk})


class FriendRequest(models.Model):

    STATUS_CHOICES = (
        ("Accepted","Accepted"),
        ("Rejected","Rejected"),
        ("Pending","Pending"),
    )

    from_user = models.ForeignKey(UserProfile, related_name=("from_user"), on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name=("to_user"), on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default="Pending", max_length=100)

    class Meta:
        verbose_name = ("FriendRequest")
        verbose_name_plural = ("FriendRequests")

    def __str__(self):
        return f"{self.from_user} -- {self.to_user}"

    def get_absolute_url(self):
        return reverse("FriendRequest_detail", kwargs={"pk": self.pk})

@receiver(post_save, sender=FriendRequest)
def FriendRequestNotification(sender, instance, created, **kwargs):

    if instance.status == "Pending":
        Notification.objects.create(from_user=instance.from_user,to_user=instance.to_user, notification_type = "Friend Request",
                                    message = f"{instance.from_user.user.username} has sent you friend request")
    else:
        Notification.objects.create(from_user=instance.to_user,to_user=instance.from_user, notification_type = "Friend Request Response",
                                    message = f"Your friend request has been {instance.status}.")


class Notification(models.Model):

    from_user = models.ForeignKey(UserProfile, related_name="notif_from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name="notif_to_user", on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=100)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Notification")
        verbose_name_plural = ("Notifications")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} from {self.from_user.user.username} to {self.to_user.user.username}"

    def get_absolute_url(self):
        return reverse("Notification_detail", kwargs={"pk": self.pk})

@receiver(post_save, sender=Notification)
def SendingNotification(sender, instance, created, **kwargs):
    # if instance.notification_type == "Friend Request":
    user_group = f"notif{instance.to_user.user.id}"
    # elif instance.notification_type == "Friend Request Response":
    #     user_group = f"notif{instance.from_user.user.id}"

    notif_async(user_group, instance)

def notif_async(user_group, instance):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        user_group,{
            "type":"send_notification",
            "notification_type":instance.notification_type,
            "from_user":instance.from_user.user.username,
            "from_user_image":instance.from_user.prof_image.name,
            "to_user":instance.to_user.user.username,
            "message":instance.message,
            "created_at":"18/02/2023"
        }
    )


class Message(models.Model):

    room = models.ForeignKey("MessageRoom", related_name=("msg_room"), on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, related_name=("Message_sender"), on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name=("Message_receiver"), on_delete=models.CASCADE)
    seen_by_users = models.ForeignKey(UserProfile, related_name=("Message_seen"), null=True, on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(upload_to="static",null=True)
    # Create a different model (Reaction) and then add foreign key there.
    # reaction = models.CharField(max_length=150, null=True)
    date = models.DateField(auto_now_add=True)


@receiver(post_save, sender=Message)
def MesageNotification(sender, instance, created, **kwargs):

    channel_layer = get_channel_layer()
    print(f"Sending message notification to {instance.receiver.user.username}")
    sender_group_name = f"notif{instance.sender.user.id}"
    receiver_group_name = f"notif{instance.receiver.user.id}"
    # async_function(sender_group_name, instance)
    async_function(receiver_group_name, instance)

    # print(f"Sending notification to {instance.receiver.username}")

def async_function(user_group, instance):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        user_group,{
            "type":"send_notification",
            "notification_type":"message_notification",
            "my_sender":instance.sender.user.username,
            "my_receiver":instance.receiver.user.username,
            "room":instance.room.group_name,
            "message":instance.message
        }
    )

    print(f"Sending notification to {user_group}")


# Create a Message Group an add fields admin_user, created, group_image

class MessageRoom(models.Model):

    group_name = models.CharField(max_length=150)
    first_user = models.ForeignKey(UserProfile, related_name=("first_user"), on_delete=models.CASCADE)
    second_user = models.ForeignKey(UserProfile, related_name=("second_user"), on_delete=models.CASCADE,null=True, blank=True)
    users_active = models.ManyToManyField(UserProfile,blank=True)
    one_to_one = models.BooleanField(default=True)
    group = models.OneToOneField("MessageGroup", on_delete=models.CASCADE, related_name="message_groups", null=True, blank=True)

    def __str__(self):
        if self.one_to_one:
            return f'{self.first_user.user} -- {self.second_user.user}'
        else:
            return f'{self.group_name}'

    
    @property
    def LatestMessage(self):
        latest_msg = Message.objects.filter(room_id=self.id).last()
        return latest_msg


    @staticmethod
    def GetGroupName(id1, id2):
        msg_room = MessageRoom.objects.filter(Q(first_user_id=id1,second_user_id=id2) | Q(first_user_id=id2, second_user_id=id1)).first()
        return msg_room

@receiver(post_save, sender=MessageRoom)
def CreateGroupName(sender, instance, created, **kwargs):
    if created and instance.one_to_one is True:
        f_user = instance.first_user.user.username
        s_user = instance.second_user.user.username
        g_n = f"{f_user}_{s_user}_{instance.first_user.user.id}_{instance.second_user.user.id}"
        MessageRoom.objects.filter(id=instance.id).update(group_name=g_n)
    elif created and instance.one_to_one is False:
        print("_____CREATING MESSAGE GROUP______")
        group_obj,m = MessageGroup.objects.get_or_create(group_admin=instance.first_user)
        instance.group = group_obj
        instance.save()


class MessageGroup(models.Model):

    group_admin = models.ForeignKey(UserProfile, related_name="group_admins", on_delete=models.CASCADE, null=True)
    created = models.DateField(auto_now_add=True)
    group_image = models.FileField(upload_to="static")

    class Meta:
        verbose_name = ("MessageGroup")
        verbose_name_plural = ("MessageGroups")

    def __str__(self):
        return self.group_admin.user.username

    def get_absolute_url(self):
        return reverse("MessageGroup_detail", kwargs={"pk": self.pk})


class MessageReaction(models.Model):

    reactions = (
        ("Smile","Smile"),
        ("Funny","Funny"),
        ("Angry","Angry"),
        ("Sad","Sad"),
        ("Crying","Crying"),
        ("Heart","Heart")
    )

    user = models.ForeignKey(UserProfile, related_name=("User_reaction"), on_delete=models.CASCADE)
    reaction = models.CharField(choices=reactions, max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("MessageReaction")
        verbose_name_plural = ("MessageReactions")

    def __str__(self):
        return self.user.user.username

    def get_absolute_url(self):
        return reverse("MessageReaction_detail", kwargs={"pk": self.pk})
