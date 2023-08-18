from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Chat

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        user = self.scope["user"]

        if user.is_authenticated:
            # Mark messages in this chat as read for the current user.
            await self.mark_messages_as_read(user)

        self.group_name = f"chat_{self.chat_id}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.mark_user_online(self.scope["user"])

        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.mark_user_offline(user)
        
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        typing = text_data_json.get('typing')

        user = self.scope["user"]
        role = user.user_type

        if message and user.is_authenticated:
            await database_sync_to_async(Message.objects.create)(
                chat_id=self.chat_id, content=message, author=user
            )
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'role': role
                }
            )

        if typing is not None:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'user_typing',
                    'typing': typing,
                    'role': role
                }
            )

    async def chat_message(self, event):
        message = event['message']
        role = event['role']
        await self.send(text_data=json.dumps({
            'message': message,
            'role': role
        }))

    async def user_typing(self, event):
        typing = event['typing']
        role = event['role']

        await self.send(text_data=json.dumps({
            'typing': typing,
            'role': role
        }))

    @database_sync_to_async
    def mark_messages_as_read(self, user):
        Message.objects.filter(chat_id=self.chat_id).exclude(author=user).update(read=True)

    @database_sync_to_async
    def get_role_for_chat(self, user):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            if user == chat.student:
                return 'S'
            elif user == chat.instructor:
                return 'I'
        except Chat.DoesNotExist:
            print("Chat not found!")
            return None

    @database_sync_to_async
    def update_user_online_status(self, user, online_status):
        chat = Chat.objects.get(id=self.chat_id)
        if user == chat.student:
            chat.student_online = online_status
        else:
            chat.instructor_online = online_status
        chat.save()

    async def mark_user_online(self, user):
        role = await self.get_role_for_chat(user)
        if role:
            if role == 'S':
                print('student')
            else:
                print('instructor')
            
            # Update the database with the online status
            await self.update_user_online_status(user, True)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'user_online',
                    'online': True,
                    'role': role
                }
            )
            print("user online")

    async def mark_user_offline(self, user):
        role = await self.get_role_for_chat(user)
        if role:
            if role == 'S':
                print('student')
            else:
                print('instructor')
            
            # Update the database with the offline status
            await self.update_user_online_status(user, False)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'user_offline',
                    'online': False,
                    'role': role
                }
            )
            print("user offline")
            
    async def user_online(self, event):
        online = event['online']
        role = event['role']
        await self.send(text_data=json.dumps({
            'online': online,
            'role': role
        }))

    async def user_offline(self, event):
        online = event['online']
        role = event['role']
        await self.send(text_data=json.dumps({
            'online': online,
            'role': role
        }))
