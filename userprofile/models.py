from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='Profile')
	# 电话号码字段
	phone = models.CharField(max_length=20, blank=True)
    # 头像
	avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 个人简介
	bio = models.TextField(max_length=500, blank=True)

   
	def __str__(self):
		return 'user {}'.format(self.user.username)