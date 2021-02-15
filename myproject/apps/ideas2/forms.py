from django import forms
from .models import Idea
class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        exclude = ["author"]
        fields = "__all__"

    def __init__(self, request, *args, **kwargs):
        
