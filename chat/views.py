from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from .models import FriendRequest, Message, MessageRoom, Notification, UserProfile
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
# from django.views.generic.base import TemplateView


class HomePageView(View):

    Model = User
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        usr = User.objects.get(id=request.user.id)
        all_usr = User.objects.exclude(id=request.user.id)
        context = {"usr":usr,"all_usr":all_usr}
        return render(request,"index.html", context)


def LoginPage(request):

    return render(request,"login.html")


def ChatRoom(request,id):

    print("GROUP_NAME")
    print(id)
    print("GROUP_NAME")
    usr = UserProfile.objects.filter(user_id=request.user.id).first()
    # usr2 = UserProfile.objects.get(id=id)

    m_room = MessageRoom.objects.filter(group_name=id).first()

    if m_room.one_to_one:
        usr2 = m_room.first_user
        if m_room.first_user == usr:
            usr2 = m_room.second_user
    else:
        usr2 = m_room

    # if not MessageRoom.objects.filter(Q(first_user=usr,second_user=usr2) | \
    #     Q(first_user=usr2,second_user=usr)).exists():
    #     MessageRoom.objects.create(first_user=usr, second_user=usr2)

    # if not MessageRoom.objects.filter(Q(first_user=usr,second_user=usr2) | \
    #     Q(first_user=usr2,second_user=usr)).exists():
    #     MessageRoom.objects.create(first_user=usr, second_user=usr2)

    # room_name = MessageRoom.GetGroupName(usr.id,usr2.id)
    msg = Message.objects.filter(room=m_room).all()
    # latest_msg = Message.objects.filter(room=room_name).last()

    # print("------------------MessageRoom-----------------")
    msgs_room = MessageRoom.objects.filter( Q (first_user=usr)| Q(second_user=usr))
    m_arr = []
    for m in msgs_room:
        messag = Message.objects.select_related("room").filter(room = m).last()
        m_arr.append(messag)
    # print("------------------MessageRoom-----------------")

    all_rooms = MessageRoom.objects.filter(Q(first_user=usr)|Q(second_user=usr)).all()

    profiles = UserProfile.objects.exclude(user=request.user)
    user_profile = UserProfile.objects.filter(user=request.user).first()
    user_notifications = Notification.objects.filter(to_user=user_profile).all()
    friend_req = FriendRequest.objects.filter(from_user=user_profile).values_list("to_user", flat=True)
    print(user_notifications)

    # No need for  ("msg",)

    context = {"msg":msg,"usr":usr,"all_usr":usr,"usr2":usr2,"room_name":m_room,"notifications":user_notifications,"all_rooms":all_rooms,
             "msgs_room":msgs_room, "msgs":m_arr, "profiles":profiles, "user_profile":user_profile, "friend_req":friend_req}

    return render(request,"chatroom_index.html", context=context)

class FileUpload(View):

    def post(self, request):
        files = request.FILES.get('files')
        msg_id = request.POST.get('message_id')
        m = Message.objects.filter(id=msg_id).first()
        m.file=files
        m.save()
        return HttpResponse("File Sucessfully added!")
