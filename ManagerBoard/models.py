from django.db import models
import datetime

# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='board/images/%Y/%m/%d', null=True, default='', blank=True)
    title = models.CharField(max_length=100, default='')
    message = models.TextField(default='No message defined')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    dateEnd = models.DateTimeField(auto_now_add=True, blank=True)
    type = models.TextField(blank=True)

    def __str__(self):
        return self.title