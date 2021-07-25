import os
from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.text import slugify

from accounts.models import Profile

# def post_thumnail_directory_path(instance, filename):
# 	thumbnail_name = 'post_{0}/thumbnail.jpg'.format(instance.pk)
# 	full_path = os.path.join(settings.MEDIA_ROOT, thumbnail_name)

# 	if os.path.exists(full_path):
# 		os.remove(full_path)

# 	return thumbnail_name

# def post_banner_directory_path(instance, filename):
# 	banner_name = 'post_{0}/banner.jpg'.format(instance.pk)
# 	full_path = os.path.join(settings.MEDIA_ROOT, banner_name)

# 	if os.path.exists(full_path):
# 		os.remove(full_path)

# 	return banner_name

# Create your models here.
class Post(models.Model):
	author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
	title = models.CharField(max_length=256)
	content = models.TextField()
	comment_count = models.PositiveIntegerField(default=0)
	views = models.PositiveIntegerField(default=0)
	thumbnail = models.ImageField(upload_to='posts/thumbnail', blank=True, null=True)
	banner = models.ImageField(upload_to='posts/banner', blank=True, null=True)
	slug = models.SlugField(max_length=256)
	created_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return self.title


	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		self.comment_count = self.comments.count()
		self.views = self.user_view.count()

		return super().save(*args, **kwargs)



class Comment(models.Model):
	author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	content = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-id']

	def __str__(self):
		return f"Comment on {self.post.title}"



class PostView(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_view')
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.profile} - {self.post}"