from django.db import models
import datetime

# Create your models here.
class WhatsappMsg(models.Model):
    author = models.CharField(max_length=100, default='')
    content = models.TextField(default='')
    creation = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.content