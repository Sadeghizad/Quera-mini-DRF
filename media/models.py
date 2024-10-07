from django.db import models
from django.conf import settings

# Quality Model
class Quality(models.Model):
    resolution = models.CharField(max_length=50)  # e.g., 1080p, 4K
    audio_type = models.CharField(max_length=50)  # e.g., stereo, surround

    def __str__(self):
        return f"{self.resolution} - {self.audio_type}"

# Actor Model
class Actor(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name

# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Country Model
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Video Model
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    story=models.TextField(null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)  # Image field for storing the poster
    trailer = models.URLField(null=True, blank=True)  # URL to the trailer video
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)  # Rating out of 10
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes
    age_restriction = models.CharField(max_length=10, blank=True, null=True)  # e.g., "PG-13"
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    subbed = models.BooleanField(default=False)
    dubbed = models.BooleanField(default=False)
    quality = models.ForeignKey(Quality, on_delete=models.SET_NULL, null=True)
    actors = models.ManyToManyField(Actor)  # Many-to-many with actors
    genres = models.ManyToManyField(Genre)  # Many-to-many with genres

    def __str__(self):
        return self.title

# Series Model
class Series(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# Season Model
class Season(models.Model):
    number = models.IntegerField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)  # One series can have many seasons

    def __str__(self):
        return f"Season {self.number} of {self.series.name}"


# Comment Model
class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.DecimalField(max_digits=3, decimal_places=1)  # Rating out of 10
    comment_rate = models.IntegerField(default=0)  # Upvotes or likes for the comment

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"

# WatchList Model
class WatchList(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Change here
    videos = models.ManyToManyField('media.Video')  # WatchList can have many videos

    def __str__(self):
        return f"{self.name} by {self.user.username}"
# UserVideoInteraction Model
class UserVideoInteraction(models.Model):
    INTERACTION_TYPE = [
        ('unseen', 'Unseen'),
        ('watched', 'Watched'),
        ('remain', 'Remain')
    ]
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPE)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # Change here
    video = models.ForeignKey('media.Video', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.video.title}"