from django.urls import re_path

from hse_task.consumers import QuizResultConsumer, AskLLMConsumer

websocket_urlpatterns = [
    re_path(
        r'ws/quiz_result/(?P<quiz_id>\d+)/$',
        QuizResultConsumer.as_asgi()),
    re_path(
        r'ws/askllm/(?P<hash_token>[^/]+)/$',
        AskLLMConsumer.as_asgi()),
]
