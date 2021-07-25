from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from accounts.models import Profile
from .models import Post, Comment, PostView
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):
	posts = Post.objects.all()

	latest_posts = Post.objects.all().order_by('-id')[:5]

	popular_posts = Post.objects.all().order_by('-views', '-id')[:5]
	

	paginator = Paginator(posts, 5)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)


	context = {
	'posts':posts_paginator,
	'recent':latest_posts,
	'popular':popular_posts,
	}

	return render(request, 'posts/post_list.html', context)


def post_detail(request, slug, pk):
	instance = get_object_or_404(Post, slug=slug, pk=pk)

	if request.user.is_authenticated:
		profile = get_object_or_404(Profile, user=request.user)
		view, created = PostView.objects.get_or_create(profile=profile, post=instance)
	
	instance.save()
	comments = Comment.objects.filter(post=instance)
	comment_form = CommentForm()

	if request.method == 'POST':
		if request.POST['content'] == '':
			pass
		else:
			content = request.POST['content']
			author = get_object_or_404(Profile, user=request.user)
			post = instance



			comment = Comment(author=author, content=content, post=post)
			comment.save()
			author.save()
			post.save()

			return redirect('post-detail', slug=instance.slug, pk=instance.pk)

	posts_from_same_author = Post.objects.filter(author=instance.author)

	context = {
	'posts_from_same_author':posts_from_same_author,
	'post':instance,
	'comments':comments,
	'form':comment_form,
	}

	return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
	form = PostForm()

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)

		author = get_object_or_404(Profile, user=request.user)
		title = request.POST['title']
		content = request.POST['content']
		thumbnail = request.FILES.get('thumbnail')
		banner = request.FILES.get('banner')

		post = Post(
			author=author, 
			title=title, 
			content=content, 
			thumbnail=thumbnail, 
			banner=banner
			)



		post.save()
		author.save()

		return redirect('post-detail', pk=post.pk, slug=post.slug)

	return render(request, 'posts/post_create.html', {
		'form':form,
		})


@login_required
def post_delete(request, slug, pk):
	instance = get_object_or_404(Post, pk=pk, slug=slug)
	author = instance.author
	title = instance.title

	if author.user != request.user:
		messages.error(request, "You are not authorised to delete this post!")
		return redirect('post-detail', slug=instance.slug, pk=instance.pk)

	if request.method == 'POST':

		instance.delete()
		author.save()

		messages.info(request, f'{title} deleted successfully!')

		return redirect('index')

	return render(request, 'posts/post_delete.html', {
		'post':instance,
		})


@login_required
def post_update(request, slug, pk):
	instance = get_object_or_404(Post, pk=pk, slug=slug)
	form = PostForm(instance=instance)

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)

		instance.title = request.POST['title']
		instance.content = request.POST['content']

		thumbnail = request.FILES.get('thumbnail')
		banner = request.FILES.get('banner')

		if thumbnail != None:
			instance.thumbnail = thumbnail

		if banner != None:
			instance.banner = banner

		instance.save()
		print(banner, thumbnail)

		return redirect('post-detail', pk=instance.pk, slug=instance.slug)


	return render(request, 'posts/post_update.html', {
		'form':form,
		'instance':instance,
		})


@login_required
def comment_update(request, pk):
	instance =get_object_or_404(Comment, pk=pk)

	if instance.author.user != request.user:
		messages.error(request, "You are not authorised to updated this comment!")
		return redirect('post-detail', pk=instance.post.pk, slug=instance.post.slug)


	if request.method == 'POST':
		instance.content = request.POST['content']

		instance.save()

		return redirect('post-detail', pk=instance.post.pk, slug=instance.post.slug)


@login_required
def comment_delete(request, pk):
	instance =get_object_or_404(Comment, pk=pk)
	post = instance.post
	author = instance.author

	if author.user != request.user:
		messages.error(request, "You are not authorised to delete this comment!")
		return redirect('post-detail', pk=post.pk, slug=post.slug)

	if request.method == 'POST':


		instance.delete()
		post.save()
		author.save()

		messages.info(request, f"Comment on {post.title} deleted successfully!")
		return redirect('post-detail', pk=post.pk, slug=post.slug)


def post_search(request):
	query = request.GET.get('query')

	if query:
		posts = Post.objects.filter(Q(title__icontains=query))

		latest_posts = Post.objects.all().order_by('-id')[:5]

		paginator = Paginator(posts, 5)
		page_number = request.GET.get('page')
		posts_paginator = paginator.get_page(page_number)

		messages.success(request, f'Results for "{query}"')

		context = {
		'posts':posts_paginator,
		'recent':latest_posts,
		}

		return render(request, 'posts/post_list.html', context)
	else:
		messages.error(request, "Please enter a valid query!")
		return redirect('index')