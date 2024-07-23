from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField as BaseCloudinaryField

# Create your models here.
class CloudinaryField(BaseCloudinaryField):
    def upload_options(self, model_instance):
        return {
            'public_id': model_instance.name,
            'filename': Post.Title,
            'unique_filename': False,
            'overwrite': True,
            'resource_type': 'auto',
            'tags': ['Post'],
            'invalidate': True,
            'quality': 'auto:eco',
        }


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Profile_pic = CloudinaryField('Profile_Pic', overwrite=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    Title = models.CharField(max_length=500)
    Descrp = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    op = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    Img = CloudinaryField('Post', resource_type="auto")
    Aww = models.IntegerField(default=0)
    Eww = models.IntegerField(default=0)

    def __str__(self):
        return self.Title


class Comment(models.Model):
    not_post_method_ok = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    op = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    Points = models.IntegerField(default=1)
    comment = models.TextField(max_length=500)
    reply = models.CharField(default='0', max_length=1)
    cmnt_chn = models.CharField(default='1', max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
