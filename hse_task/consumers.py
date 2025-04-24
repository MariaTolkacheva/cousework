import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer


class QuizResultConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.quiz_id = self.scope['url_route']['kwargs']['quiz_id']
        # self.group_name = f"quiz_result_{self.user_id}_{self.quiz_id}"
        self.group_name = "quiz_result_1_1"
        logging.info("[CONNECT] %s, user_id=%s, quiz_id=%s, group_name=%s",
                     self.channel_layer, self.user_id, self.quiz_id, self.group_name)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logging.info('disconnecting from QuizResultConsumer')
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_result(self, event):
        logging.info('[QuizResultConsumer DISCONNECT]')
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


class AskLLMConsumer(AsyncWebsocketConsumer):
    """Consumer for asking a model"""

    async def connect(self):
        self.question_hash = self.scope['url_route']['kwargs']['hash_token']
        self.group_name = f"askllm_{self.question_hash}"
        logging.info("[AskLLMConsumer CONNECT] %s, question_hash=%s, group_name=%s",
                     self.channel_layer, self.question_hash, self.group_name)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logging.info('[AskLLMConsumer DISCONNECT]')
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_result(self, event):
        logging.info('sending result from AskLLMConsumer')
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
