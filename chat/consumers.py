import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, MessageRoom
from django.contrib.auth.models import User
import time

class ChatConsumer(WebsocketConsumer):

    users_dict = {}

    def connect(self, data):

        # usr = User.objects.filter(availability=True, user_type="Employee")

        r_id = self.scope['path'].split('socket-server/room_id=')[1].split("_")
        group_name = self.GetGroupName(r_id[0], r_id[1])
        print(self.__dict__)
        # ChatConsumer.users_dict[group_name] = []

        self.room_group_name = f"chat_{group_name.group_name}"
        print("-----------")
        print(group_name)
        print("-----------")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

        # self.send(
        #     text_data=json.dumps({
        #         'type':'Connection Established!',
        #         'message':'You are now connected Sir!'
        #     })
        # )

    def GetGroupName(self, id1, id2):

        m1 = MessageRoom.objects.filter(first_user_id__in=id1, second_user_id__in=id2).first()
        m2 = MessageRoom.objects.filter(first_user_id__in=id2, second_user_id__in=id1).first()

        if m1:
            print("Room_id Exists 1= " + str(m1))
            group_name = m1
        elif m2:
            print("Room_id Exists 2= " + str(m2))
            group_name = m2

        return group_name


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print("--------------TEXT DATA JSON-------------------")
        # print(text_data_json)
        # print("--------------TEXT DATA JSON-------------------")
        username = text_data_json['username']
        room_id = text_data_json['room_id'].split("_")

        try:
            msg = text_data_json['typing']

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'typing_message',
                    'message':msg,
                    'username':username
                }
            )

        except:
            receiver = text_data_json['receiver']
            msg = text_data_json['message']
            msg_id = text_data_json['message_id']

            if not msg_id:

                self.save_messages(username,receiver,room_id,msg)
                print(msg)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'chat_message',
                        'message':msg,
                        'username':username
                    }
                )
            elif msg_id:
                print("editing the message")
                self.edit_message(msg_id, msg)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'update_chat_message',
                        'message':msg,
                        'msg_id':msg_id,
                        'receiver':receiver
                    }
                )

    def update_chat_message(self, event):

        msg = event['message']
        msg_id = event['msg_id']
        msg_receiver = event['receiver']
        self.send(
            text_data=json.dumps({
                'type':'update_chat',
                'message':msg,
                'msg_id':msg_id,
                'receiver':msg_receiver
            })
        )

    def chat_message(self, event):

        msg = event['message']
        username = event['username']
        self.send(
            text_data=json.dumps({
                'type':'chat',
                'message':msg,
                'username':username
            })
        )

    def typing_message(self, event):

        msg = event['message']
        username = event['username']
        print("User is typing........")

        self.send(
            text_data=json.dumps({
                'type':'typing_status',
                'message':msg,
                'username':username
            })
        )


    def save_messages(self, username, receiver, room, msg):
        sender = User.objects.filter(username=username).first()
        receiver = User.objects.filter(id=receiver).first()
        room = self.GetGroupName(room[0], room[1])

        m = Message.objects.create(sender=sender,receiver=receiver,room=room,message=msg)

    def edit_message(self, msg_id, msg):
        m = Message.objects.filter(id=msg_id).update(message=msg)



class UserChatConsumer(WebsocketConsumer):

    def connect(self):

        r_id = self.scope['path'].split('/ws/user_chat/room_id=')[1]
        # group_name = self.GetGroupName(r_id[0], r_id[1])
        self.room_name = "test_room"
        self.room_group_name = f"notif{r_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()
        print(f"connected to the test consumers ---- {self.room_group_name}")


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print("-----Notif------")
        # print(text_data_json)
        # print("-----Notif------")


    def send_notification(self, event):

        print("-----Notif------")
        print(event)
        print("-----Notif------")

        self.send(
            text_data=json.dumps({
                'type':'notifications',
                'message':event,
            })
        )
