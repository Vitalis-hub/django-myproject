from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from myproject.apps.core.models import (CreationModificationDateBase, MetaTagsBase, UrlBase, )
from django.conf import settings
from django.core.exceptions import ValidationError
import re
from myproject.apps.core.model_fields import (
    MultilingualCharField,
    MultilingualTextField,
)

'''
class Idea(CreationModificationDateBase, MetaTagsBase, UrlBase):
    pass
'''

class Idea(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        #is a value with a value such as "auth_User"
        verbose_name=_("Author"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name ="authored_ideas2",

    )

    title = MultilingualCharField(
        _("Title"),
        max_length = 200
    )

    content = MultilingualTextField(
        _("Content"),
    )

    category = models.ForeignKey(
        "categories.Category",
        verbose_name=_("Category"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="category_ideas",
    )

    categories = models.ManyToManyField(
        "categories.Category",
        verbose_name = _("Categories"),
        blank=True,
        related_name = "ideas",
    )

    class Meta:
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")
        constraints = [
            models.UniqueConstraint(
                fields=["title"],
                condition=~models.Q(author=None),
                name="unique_titles_for_each_author",
            ),
            models.CheckConstraint(
                check=models.Q(
                    title__iregex=r"^\S.*\S$"
                ),
                name="title_has_no_leading_and_trailing_whitespaces",
            )
        ]

    def str(self):
        return self.title    

    def clean(self):
        import re

        if self.author and Idea.objects.exclude(pk=self.pk).filter(
            author=self.author,
            title=self.title,
        ).exists():
            raise ValidationError(
                _("Each idea of the same user should have a unique title")
            )
        if not re.match(r"^\S.*\S$", self.title):
            raise ValidationError(
                _("The title cannot start or end with a whhitespace.")
        )


class IdeaTranslations(models.Model):
    idea = models.ForeignKey(
        Idea,
        verbose_name = _("Idea"),
        on_delete=models.CASCADE,
        related_name ="translations",
    )
    language = models.CharField(_("Language"), max_length=7)

    title = models.CharField(
        _("Title"), 
        max_length=200
    )
    content = models.TextField(
        _("Content")
    )

    class Meta:
        verbose_name = _("Idea Translations")
        verbose_name_plural = _("Idea Translations")
        ordering = ["language"]
        unique_together = [["idea", "language"]]

    def __str__(self):
        return self.title

from myproject.apps.core.models import (
    object_relation_base_factory as generic_relation,
)

FavoriteObjectBase = generic_relation(
    is_required=True,
)

OwnerBase = generic_relation(
    prefix="owner",
    prefix_verbose=_("Owner"),
    is_required=True,
    add_related_name=True,
    limit_content_type_choices_to={
        "model__in":(
            "user",
            "group",
        )
    }
)

class Like(FavoriteObjectBase, OwnerBase):
    class Meta:
        verbose_name = _("Like"), 
        verbose_name_plural = _("Likes")

    def __str__(self):
        return _("{owner} likes {object}").format(
            owner=self.owner_content_object,
            object=self.content_object
        )



 
