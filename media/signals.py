from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment,UserVideoInteraction
from django.db import models

@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)  # Handle when comments are deleted, too
def update_video_rating(sender, instance, **kwargs):
    video = instance.video
    # Get all the comments related to this video and calculate the average rating
    comments = Comment.objects.filter(video=video)
    if comments.exists():
        avg_rating = comments.aggregate(models.Avg('rate'))['rate__avg']
        video.rating = avg_rating
    else:
        video.rating = None  # Reset rating if no comments
    video.save()

@receiver(post_save, sender=UserVideoInteraction)
def update_video_views(sender,instance,*args, **kwargs):
    video = instance.video
    video.views = UserVideoInteraction.objects.filter(video=video).count()
    video.save()