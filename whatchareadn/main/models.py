from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Shelves(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Books(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    authors = models.CharField(max_length=250, null=True, blank=True)
    googleid = models.CharField(max_length=250)
    image_link = models.URLField(max_length=1000, null=True, blank=True)
    have_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
