from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class articlePost(models.Model):
	class Meta:
		ordering=('-created',)

	title=models.CharField(max_length=100)
	body = models.TextField()
	created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title