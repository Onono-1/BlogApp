from PIL import Image
import os

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save


def user_directory_path(instance, filename):
    profile_pic_name = 'profiles/user_{0}/profile.jpg'.format(instance.user.pk)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    post_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    bio = models.TextField(default='No mentioned')
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']


    def __str__(self):
        return self.user.username


    def save(self, *args, **kwargs):
        self.post_count = self.posts.count()
        self.comment_count =self.comments.count()
        self.views = self.view_count.count()


        super().save(*args, **kwargs)
        SIZE = 112, 112

        if self.image:
            pic = Image.open(self.image.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.image.path, format='PNG')



class ProfileView(models.Model):
    viewed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='view_count')
    viewer = models.ForeignKey(Profile, on_delete=models.CASCADE)



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)