from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PTTArticle(models.Model):
    author = models.CharField(max_length=100)
    board = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
