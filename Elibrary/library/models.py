from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.TextChoices):
    FICTION = 'fiction'
    SELF_HELP = 'self_help'
    HISTORY = 'history'
    CRIME = 'crime'
    THRILLER = 'thriller'
    HORROR = 'horror'
    SCIENCE = 'science'
    BIOGRAPHY = 'biography'
    BUSINESS = 'business'
    PHILOSOPHY = 'philosophy'
    POLITICS = 'politics'
    CLASSICS = 'classics'
    COMPUTERS = 'computers'
    

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description = models.TextField()
    file = models.FileField(upload_to='books/', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.FICTION)
    cover = models.URLField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        db_table = 'books'
        indexes = [models.Index(fields=['title'])]
