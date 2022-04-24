from django.db import models
from django.contrib.auth.models import User
from myapp.models import articlePost

# Create your models here.

class articleComment(models.Model):
	body=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
	article=models.ForeignKey(articlePost,on_delete=models.CASCADE,related_name='comments')

	class Meta:
		ordering=('-created',)

	def __str__(self):
		return self.body[:20]