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
from rest_framework.permissions import IsAuthenticated, AllowAny


class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()


class QualityViewSet(viewsets.ModelViewSet):
    serializer_class = QualitySerializer
    queryset = Quality.objects.all()


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class SerieViewSet(viewsets.ModelViewSet):
    serializer_class = SeriesSerializer
    queryset = Series.objects.all()


class SeasonViewSet(viewsets.ModelViewSet):
    serializer_class = SeasonSerializer
    queryset = Season.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    def get_queryset(self):
        # Get all comments and filter by 'video_id' if it's passed as a query parameter
        queryset = Comment.objects.all()
        video_id = self.request.query_params.get('video_id', None)
        if video_id is not None:
            queryset = queryset.filter(video_id=video_id)
        return queryset

    def perform_create(self, serializer):
        video_id = self.request.query_params.get('video_id', None)
        serializer.save(user=self.request.user, video_id=int(video_id))


class WatchListViewSet(viewsets.ModelViewSet):
    serializer_class = WatchListSerializer
    queryset = WatchList.objects.all()


class UserVideoInteractionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserVideoInteractionSerializer

    def get_queryset(self):
        return UserVideoInteraction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the authenticated user to the UserVideoInteraction
        serializer.save(user=self.request.user)
