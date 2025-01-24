from turtle import title
from unicodedata import category
from django.db import models
from accounts.models import CustomUser
from ckeditor.fields import RichTextField 
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    title = models.CharField(max_length=255 , blank=True )
    title_pic = models.ImageField(upload_to='category/' , blank=True)
    short_description = models.CharField(max_length=255 , blank=True)
    body = RichTextField(blank=True , null=True )
    post_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.IntegerField(blank=True , null=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    author = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    title = models.CharField(max_length=255 , blank=True )
    title_pic = models.ImageField(upload_to='category/' , blank=True)
    short_description = models.CharField(max_length=255 , blank=True)
    body = RichTextField(blank=True , null=True )
    post_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.title

class items(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    session = models.CharField(max_length=255)

class Comments (models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name='comments')
    name = models.CharField(max_length=255)
    gmail = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateField(auto_now_add=True , null=True)

    def __str__(self):
        return self.post.title


class BannerPosts(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)


    def __str__(self):
        return self.post.title


class FeaturedPost(models.Model):

    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    


    def __str__(self):
        return self.post.title


class FeaturedCategory (models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    pic = models.ImageField(upload_to = 'featuredpic/' , blank=True)

    def __str__(self):
        return self.category.name

class FooterCategory (models.Model):

    category = models.ForeignKey(Category , on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name
