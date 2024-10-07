from rest_framework.routers import DefaultRouter
from .viewsets import *
from django.urls import path, include
router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'qualitys', QualityViewSet, basename='quality')
router.register(r'actors', ActorViewSet, basename='actor')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'countrys', CountryViewSet, basename='country')
router.register(r'series', SerieViewSet, basename='serie')
router.register(r'seasons', SeasonViewSet, basename='season')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'watchLists', WatchListViewSet, basename='watchList')
router.register(r'uservideointeractions', UserVideoInteractionViewSet, basename='uservideointeraction')

urlpatterns = [
    path('', include(router.urls)),
]