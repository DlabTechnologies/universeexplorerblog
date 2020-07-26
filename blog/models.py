from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from account.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField




class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")

class Post(models.Model):
    objects = models.Manager() #our default manager
    published = PublishedManager() #our custom model manager
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published','Published'),
    )
    title       =       models.CharField(max_length=150)
    slug        =       models.SlugField(max_length=150)
    author      =       models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body        =       RichTextField()
    image       =       models.ImageField(upload_to='post_images/', blank=True, null=True)
    likes       =       models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)
    heart       =       models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='heart', blank=True)
    created     =       models.DateTimeField(auto_now_add=True)
    updated     =       models.DateTimeField(auto_now=True)
    status      =       models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    restrict_comment = models.BooleanField(default=False)
    favourite   =       models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favourite', blank=True)
    tags        =       TaggableManager()
    blog_views =        models.IntegerField(default=0)
    


    
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.id, self.slug])

    def get_absolute_urlr(self):
        return reverse("blog:post_edit", args=[self.id, self.slug])


    
    
    def total_likes(self):
        return self.likes.count()

    def total_heart(self):
        return self.heart.count()



@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name="replies", on_delete=models.CASCADE)
    content = models.TextField(max_length=600)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))

class ContactForm(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=300)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class NewsletterSignup(models.Model):
    email = models.EmailField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email