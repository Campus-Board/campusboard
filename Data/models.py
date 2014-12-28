from django.db import models
import pickle
from Personalization import constants
class Message(models.Model):
    author = models.CharField(max_length=30)
    content = models.CharField(max_length=255)
    creation = models.DateTimeField(auto_now_add=True, blank=True)

class User(models.Model):
    phone_number = models.CharField(max_length=30, unique=True)
    bluetooth_id = models.CharField(max_length=30, unique=True)
    alias = models.CharField(max_length=30)
    profile = models.CharField(max_length=1000, default='None')
    @property
    def profile(self):
        if(self.profile == 'None'):
            return constants.default_profile()
        else:
            return pickle.loads(self.profile)
    @profile.setter
    def profile(self, profile_array):
        self.profile = pickle.dumps(profile_array)


