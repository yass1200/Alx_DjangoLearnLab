from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb: str, target=None):
    n = Notification(recipient=recipient, actor=actor, verb=verb)
    if target is not None:
        n.target_content_type = ContentType.objects.get_for_model(target.__class__)
        n.target_object_id = target.pk
    n.save()
    return n
