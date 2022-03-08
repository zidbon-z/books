from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Shelf(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    selflink = models.URLField(max_length=1000, null=True, blank=True)
    title = models.CharField(max_length=250)
    authors = models.CharField(max_length=250, null=True, blank=True)
    isbn10 = models.CharField(max_length=10, null=True, blank=True)
    isbn13 = models.CharField(max_length=13, null=True, blank=True)
    description = models.CharField(max_length=20000, null=True, blank=True)
    googleid = models.CharField(max_length=250)
    image_link = models.URLField(max_length=1000, null=True, blank=True)
    have_read = models.BooleanField(default=False)
    reading = models.BooleanField(default=False)
    owned = models.BooleanField(default=False)
    shelf = models.ForeignKey(Shelf, related_name='books', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
