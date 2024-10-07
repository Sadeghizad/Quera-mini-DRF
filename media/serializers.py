from rest_framework import serializers
from .models import *


class VideoSerializer(serializers.ModelSerializer):
    actors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all()
    )  # Adjust this based on your need
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all()
    )  # Adjust this based on your need

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "description",
            "poster",
            "trailer",
            "rating",
            "release_date",
            "duration",
            "age_restriction",
            "country",
            "subbed",
            "dubbed",
            "quality",
            "actors",
            "genres",
        ]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name", "bio"]


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ["id", "name", "description"]


class SeasonSerializer(serializers.ModelSerializer):
    series = SeriesSerializer()  # Optionally nest the Series

    class Meta:
        model = Season
        fields = ["id", "number", "series"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "video", "user", "text", "rate", "comment_rate"]


class WatchListSerializer(serializers.ModelSerializer):
    videos = serializers.PrimaryKeyRelatedField(many=True, queryset=Video.objects.all())

    class Meta:
        model = WatchList
        fields = ["id", "name", "user", "videos"]


class QualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quality
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class UserVideoInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVideoInteraction
        fields = "__all__"
