from django import forms
from . models import articlePost

class articlepostform(forms.ModelForm):
	class Meta:
		model=articlePost
		fields=('title','body')