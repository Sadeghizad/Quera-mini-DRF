from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/videos/<int:video_id>/', consumers.VideoConsumer.as_asgi()),
]
