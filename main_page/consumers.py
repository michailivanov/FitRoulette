import asyncio
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from .models import GameSession


class GameSessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f'game_session_{self.session_id}'

        # Добавляем нового пользователя в группу
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # Обновляем количество пользователей
        await self.update_user_count(True)

    async def disconnect(self, close_code):
        # Удаляем пользователя из группы
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        # Обновляем количество пользователей
        await self.update_user_count(False)

    async def update_user_count(self, connect):
        user_count_key = f'user_count_game_session_{self.session_id}'

        # Проверяем, существует ли ключ в кеше
        if not cache.get(user_count_key):
            cache.set(user_count_key, 0)  # Инициализируем ключ с нулевым значением

        # Управление счетчиком пользователей через кеш
        if connect:
            user_count = cache.incr(user_count_key)
        else:
            user_count = cache.decr(user_count_key)
            # В случае отрицательного количества пользователей, сбрасываем на 0
            if user_count < 0:
                cache.set(user_count_key, 0)
                user_count = 0

        # Отправка сообщения всем в группе
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'user_count_message',
                'count': user_count
            }
        )

    async def user_count_message(self, event):
        # Отправка количества пользователей в WebSocket
        await self.send(text_data=json.dumps({
            'user_count': event['count']
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'start_game':
            # Отправка сообщения о перенаправлении всем подключенным пользователям
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'start_game',
                }
            )
        if action == 'spin_wheel':
            game_session = await self.get_game_session()
            exercises = game_session.shuffled_exercises
            current_index = (game_session.current_exercise_index + 1) % len(exercises)
            await self.update_game_session_index(current_index)  # Обновляем индекс в базе данных

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'exercise_selected',
                    'name': exercises[current_index]['name']
                }
            )

    @database_sync_to_async
    def get_game_session(self):
        return GameSession.objects.get(session_id=self.session_id)

    @database_sync_to_async
    def update_game_session_index(self, index):
        session = GameSession.objects.get(session_id=self.session_id)
        session.current_exercise_index = index
        session.save()

    async def start_game(self, event):
        # Отправка сообщения о перенаправлении назад в WebSocket
        await self.send(text_data=json.dumps({
            'command': 'redirect',
            'url': f'/start_game/{self.session_id}/'
        }))

    async def exercise_selected(self, event):
        # Извлекаем информацию из события
        exercise_name = event['name']

        # Отправляем название упражнения клиентам через WebSocket
        await self.send(text_data=json.dumps({
            'command': 'display_exercise',
            'name': exercise_name
        }))