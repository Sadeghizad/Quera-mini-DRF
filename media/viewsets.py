from rest_framework import viewsets
from .models import (
    Video,
    Quality,
    Actor,
    Genre,
    Country,
    Series,
    Season,
    Comment,
    WatchList,
    UserVideoInteraction,
)
from .serializers import (
    VideoSerializer,
    QualitySerializer,
    ActorSerializer,
    GenreSerializer,
    CountrySerializer,
    SeriesSerializer,
    SeasonSerializer,
    CommentSerializer,
    WatchListSerializer,
    UserVideoInteractionSerializer,
)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.permissions import IsAuthenticated, AllowAny
from mini2.permissions import IsAdminOrReadOnly
from mini2.permissions import IsOwnerOrAdmin
class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()


class QualityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = QualitySerializer
    queryset = Quality.objects.all()


class ActorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class SerieViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SeriesSerializer
    queryset = Series.objects.all()


class SeasonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SeasonSerializer
    queryset = Season.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin,IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    def get_queryset(self):
        
        queryset = Comment.objects.all()
        video_id = self.request.query_params.get('video_id', None)
        if video_id is not None:
            queryset = queryset.filter(video_id=video_id)
        return queryset

    def perform_create(self, serializer):
        video_id = self.request.query_params.get('video_id', None)
        comment = serializer.save(user=self.request.user, video_id=int(video_id))
        
        # Broadcast the new comment via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'comments',
            {
                'type': 'comment_message',
                'comment': {
                    'id': comment.id,
                    'text': comment.text,
                    'user': comment.user.username,
                    'video': comment.video.id,
                    'created_at': comment.created_at.isoformat(),
                }
            }
        )
class WatchListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = WatchListSerializer
    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserVideoInteractionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = UserVideoInteractionSerializer

    def get_queryset(self):
        return UserVideoInteraction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)
