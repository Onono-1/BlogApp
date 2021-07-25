from django.urls import path

from . import views

urlpatterns = [
	path('', views.post_list, name='index'),
	path('new/', views.post_create, name='post-create'),
	path('<str:slug>-<int:pk>/', views.post_detail, name='post-detail'),
	path('<str:slug>-<int:pk>/update/', views.post_update, name='post-update'),
	path('<str:slug>-<int:pk>/delete/', views.post_delete, name='post-delete'),
	path('<int:pk>/update/', views.comment_update, name='comment-update'),
	path('<int:pk>/delete/', views.comment_delete, name='comment-delete'),
	path('post_search/', views.post_search, name='post-search'),
]