from django.db import models
from django.contrib.auth.models import User
# Create your views here.

class Blog(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    tagsv= models.ManyToManyField('Tag', blank=True)

    class Meta:
            indexes = [
                models.Index(fields=['title'], name='title_idx'),
                models.Index(fields=['content'], name='content_idx'),
                models.Index(fields=['title', 'content'], name='fulltext_idx'),
            ]

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__t(self):
        return f'Comment by {self.author}'
    
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

