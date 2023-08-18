from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
	username = models.CharField(max_length = 30, unique = True)
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	date_joined = models.DateTimeField(auto_now_add = True)
	image = models.ImageField(upload_to = 'media', blank = True, default = 'media/avatar.png')
	
	USERNAME_FIELD = 'username'  # Теперь используем username как поле для входа
	REQUIRED_FIELDS = ['first_name', 'last_name']
	
	def __str__(self):
		return self.username