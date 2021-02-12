import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from myproject.apps.core.model_fields import TranslatedField
from myproject.apps.core.models import (
    CreationModificationDateBase, UrlBase
)

RATING_CHOICES = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

class Idea(CreationModificationDateBase, UrlBase):
    uuid = model.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    author = model.ForiegnKey(
        settings.AUTH_USER_MODEL,
        verbose_name = ('Author')
    )
