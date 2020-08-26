from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Message(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=False, verbose_name='姓名')
    tellphone = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    mess = models.CharField(max_length=1024, unique=False, verbose_name='留言信息')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




