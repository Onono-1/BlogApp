from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User

from .forms import ProfileUpdateForm, SignUpForm
from .models import Profile, ProfileView
from posts.models import Post, Comment


def profile_list(request):
	profies = Profile.objects.all()

	latest_profiles = Profile.objects.all().order_by('-id')[:5]
	popular_profiles = Profile.objects.all().order_by('-views', '-id')[:5]

	paginator = Paginator(profies, 5)
	page_number = request.GET.get('page')
	profiles_paginator = paginator.get_page(page_number)

	context = {
	'profiles':profiles_paginator,
	'recent':latest_profiles,
	'popular':popular_profiles,
	}

	return render(request, 'accounts/profile_list.html', context)



@login_required
def profile_update(request, username):
	user = get_object_or_404(User, username=username)
	instance = get_object_or_404(Profile, user=user)
	form = ProfileUpdateForm(instance=instance)

	if instance.user.username != request.user.username:
		messages.error(request, 'You are not authorised to update this profile!')
		return redirect('index')

	if request.method == 'POST':
		form = ProfileUpdateForm(request.POST)
		image = request.FILES.get('image')

		if form.is_valid():
			if image != None:
				instance.image = image
			instance.facebook = form.cleaned_data['facebook']
			instance.github = form.cleaned_data['github']
			instance.youtube = form.cleaned_data['youtube']
			instance.bio = form.cleaned_data['bio']

			instance.save()

			return redirect('profile-detail', username=request.user.username)


	return render(request, 'accounts/profile_update.html', {
		'form':form,
		})


def profile_detail(request, username):
	user = get_object_or_404(User, username=username)
	instance = get_object_or_404(Profile, user=user)

	if request.user.is_authenticated:
		active_profile = get_object_or_404(Profile, user=request.user)
		view, created = ProfileView.objects.get_or_create(viewed=instance, viewer=active_profile)
	
	instance.save()

	user_posts = Post.objects.filter(author=instance)
	user_comments = Comment.objects.filter(author=instance)

	paginator = Paginator(user_posts, 5)
	page_number = request.GET.get('page')
	user_posts_paginator = paginator.get_page(page_number)

	paginator = Paginator(user_comments, 5)
	page_number = request.GET.get('page')
	user_comments_paginator = paginator.get_page(page_number)

	context = {
	'profile':instance,
	'posts':user_posts_paginator,
	'comments':user_comments_paginator,
	}

	return render(request, 'accounts/profile_detail.html', context)


def register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			
			messages.success(request, "Account created Successfully, Please Login!")

			return redirect('login')
	else:
		form = SignUpForm()
	
	context = {
		'form':form,
	}

	return render(request, 'accounts/register.html', context)


@login_required
def user_search(request):
	query = request.GET.get('query')
	# latest_profiles = Profile.objects.all().order_by('-id')[:5]

	if query:
		users = User.objects.filter(Q(username__icontains=query))
		print(users)

		profiles = []
		for user in users:
			profile = get_object_or_404(Profile, user=user)
			profiles.append(profile)
			print(profile)


		latest_profiles = Profile.objects.all().order_by('-id')[:5]

		paginator = Paginator(profiles, 5)
		page_number = request.GET.get('page')
		profiles_paginator = paginator.get_page(page_number)

		messages.success(request, f"Results for '{query}'")


		context = {
		'profiles':profiles_paginator,
		'recent':latest_profiles,
		}

		return render(request, 'accounts/profile_list.html', context)

	else:
		# profiles = Profile.objects.all()

		# paginator = Paginator(profiles, 5)
		# page_number = request.GET.get('page')
		# profiles_paginator = paginator.get_page(page_number)

		messages.error(request, 'Please enter a valid query!')
		return redirect('profile-list')

		# context ={
		# 'profiles':profiles_paginator,
		# 'recent':latest_profiles
		# }
		# return render(request, 'accounts/profile_list.html', context)