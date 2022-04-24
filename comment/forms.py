from django import forms
from . models import articleComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = articleComment
        fields = ['body']