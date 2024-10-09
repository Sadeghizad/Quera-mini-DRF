from django.urls import path
from . import consumers
from django.urls import re_path
from .consumers import CommentConsumer
websocket_urlpatterns = [
    path('ws/videos/<int:video_id>/', consumers.VideoConsumer.as_asgi()),
    re_path(r'^comments/$', CommentConsumer.as_asgi()),
]