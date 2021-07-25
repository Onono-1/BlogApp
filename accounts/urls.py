from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm

from . import views

urlpatterns = [
	path('users/', views.profile_list, name='profile-list'),
	path('user/<str:username>/', views.profile_detail, name='profile-detail'),
	path('user/<str:username>/update/', views.profile_update, name='profile-update'),
	path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', form_class=LoginForm), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), {'next_page':'index'}, name='logout'),
	path('register/', views.register, name='register'),
	path('user_search/', views.user_search, name='user-search'),
	path('passwordreset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   	path('passwordreset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   	path('passwordreset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   	path('passwordchange/', auth_views.PasswordChangeView.as_view(), name='password_change'),
   	path('passwordchange/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]