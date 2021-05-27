from django.db import models

# Create your models here.
class user(models.Model):
    username=models.CharField(max_length=256,primary_key=True)
    password=models.CharField(max_length=256)
    c_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['c_time']
        verbose_name='用户'
        verbose_name_plural='用户'