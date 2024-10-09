from rest_framework import serializers
from .models import *


class VideoSerializer(serializers.ModelSerializer):
    actors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all()
    )  
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all()
    )  

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
    series = SeriesSerializer()  

    class Meta:
        model = Season
        fields = ["id", "number", "series"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["user", "text", "rate", "comment_rate"]
        extra_kwarg = {"user": {"requierd": False}}
        read_only_fields = ["user"]

    def get_user(self, obj):
        return obj.user.username

class WatchListSerializer(serializers.ModelSerializer):
    videos = serializers.PrimaryKeyRelatedField(many=True, queryset=Video.objects.all())
    user = serializers.SerializerMethodField()
    class Meta:
        model = WatchList
        fields = ["name", "user", "videos"]
        read_only_fields = ["user"]
    def get_user(self, obj):
        return obj.user.username


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
        fields = ["date", "video", "last_minute"]
