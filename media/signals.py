from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment, UserVideoInteraction, Video
from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)  # Handle when comments are deleted, too
def update_video_rating(sender, instance, **kwargs):
    video = instance.video
    # Get all the comments related to this video and calculate the average rating
    comments = Comment.objects.filter(video=video)
    if comments.exists():
        avg_rating = comments.aggregate(models.Avg("rate"))["rate__avg"]
        video.rating = avg_rating
    else:
        video.rating = None  # Reset rating if no comments
    video.save()


@receiver(post_save, sender=UserVideoInteraction)
def update_video_views(sender, instance, *args, **kwargs):
    video = instance.video
    video.views = UserVideoInteraction.objects.filter(video=video).count()
    video.save()


@receiver(post_save, sender=Video)
def video_updated(sender, instance, **kwargs):
    # When a video is updated, broadcast the changes via WebSocket
    send_video_update(instance)


def send_video_update(video):
    """Send WebSocket update for the video."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"video_{video.id}",  # Group name based on video ID
        {
            "type": "video_update",
            "action": "update_views",  # Example action
            "data": {
                "views": video.views,
                "rating": str(
                    video.rating
                ),  # Ensure DecimalField is serialized as string
                "title": video.title,
                "poster": video.poster.url if video.poster else None,
                "trailer": video.trailer,
                "duration": video.duration,
                "release_date": video.release_date.strftime("%Y-%m-%d"),
            },
        },
    )
