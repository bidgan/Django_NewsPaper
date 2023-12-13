from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)
        self.rating = 0
        self.posts = []

    def update_rating(self):
        # Суммарный рейтинг статей автора, умноженный на 3
        rating_posts = sum(post.rating for post in self.posts) * 3
        # Суммарный рейтинг комментариев автора
        rating_comments = sum(
            comment.rating for post in self.posts for comment in post.comments if comment.author == self)
        # Суммарный рейтинг комментариев к статьям автора
        rating_comments_posts = sum(comment.rating for post in self.posts for comment in post.comments)

        # Обновление общего рейтинга автора
        self.rating = rating_posts + rating_comments + rating_comments_posts

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_TYPES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255,default ='Default title',verbose_name = 'Заголовок')
    content = models.CharField(max_length=2048,default='default content',verbose_name ='Контент')
    rating = models.IntegerField(default=0)

    def __init__(self, *args,**kwargs):
        super(Post,self).__init__(*args,**kwargs)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        return self.content[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __init__(self, *args,**kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1
