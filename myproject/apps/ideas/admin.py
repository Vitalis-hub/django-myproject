from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from myproject.apps.core.admin import LanguageChoicesForm
from myproject.apps.core.admin import get_multilingual_field_names
from .models import Idea, IdeaTranslations

class IdeaTranslationsForm(LanguageChoicesForm):
    class Meta:
        model = IdeaTranslations
        fields = "__all__"

class IdeaTranslationsInline(admin.StackedInline):
    form = IdeaTranslationsForm
    model = IdeaTranslations
    extra = 0

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    inlines = [IdeaTranslationsInline]
    
    fieldsets = [
        (_("Title and Content"), {
            "fields": ["title", "content"]
        }),
    ]