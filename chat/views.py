from django.shortcuts import render
from .models import Message, MessageRoom
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
# Create your views here.



class HomePageView(View):

    Model = User
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        usr = User.objects.get(id=request.user.id)
        all_usr = User.objects.exclude(id=request.user.id)
        context = {"usr":usr,"all_usr":all_usr}
        return render(request,"index.html", context)

    #     return HttpResponse('GET request!')

    # def post(self, request, *args, **kwargs):
    #     return HttpResponse('POST request!')
    
    

    # return render(request,"index.html", context={"usr":usr,"all_usr":all_usr})


def ChatRoom(request,id):

    usr = User.objects.get(id=request.user.id)
    usr2 = User.objects.get(id=id)
    
    if not MessageRoom.objects.filter(first_user=usr, second_user=usr2).exists() and \
           not MessageRoom.objects.filter(first_user=usr2, second_user=usr).exists():
        msg_room = MessageRoom.objects.create(first_user=usr, second_user=usr2)

    room_name = GetGroupName(usr,usr2)
    msg = Message.objects.filter(room=room_name).all()
    latest_msg = Message.objects.filter(room=room_name).last()

    # print("------------------MessageRoom-----------------")
    msgs_room = MessageRoom.objects.filter( Q (first_user=usr)| Q(second_user=usr))
    m_arr = []
    for m in msgs_room:
        messag = Message.objects.select_related("room").filter(room = m).last()
        m_arr.append(messag)
    # print("------------------MessageRoom-----------------")

    print(request.user)
    all_usr = User.objects.exclude(id=request.user.id)
    context = {"msg":msg,"usr":usr,"all_usr":all_usr,"usr2":usr2, "room_name":room_name, "msgs_room":msgs_room, "msgs":m_arr}

    return render(request,"chatroom_index.html", context=context)


def GetGroupName(u1, u2):

    m1 = MessageRoom.objects.filter(first_user=u1, second_user=u2).first()
    m2 = MessageRoom.objects.filter(first_user=u2, second_user=u1).first()

    if m1:
        print("Room_id Exists 1= " + str(m1))
        group_name = m1
    elif m2:
        print("Room_id Exists 2= " + str(m2))
        group_name = m2

    return group_name

