from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image','facebook','github','youtube','bio']

		widgets = {
			'image':forms.FileInput(attrs={'class':'form-control'}),
			'facebook':forms.URLInput(attrs={'class':'form-control'}),
			'github':forms.URLInput(attrs={'class':'form-control'}),
			'youtube':forms.URLInput(attrs={'class':'form-control'}),
			'bio':forms.Textarea(attrs={'class':'form-control'}),
			
		}



def ForbiddenUsers(value):
	forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
	if value.lower() in forbidden_users:
		raise ValidationError(f'Invalid name for user, {value} is a reserverd word.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this username already exists.')


class SignUpForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'Username'}), max_length=30, required=True,)
	email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'name@gmail.com'}), max_length=100, required=True,)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'Password'}), required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'Confirm Password'}), required=True)

	class Meta:
		model = User
		fields = ['username','email','password','confirm_password']

		# widgets = {
		# 	'username':forms.TextInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'Username'}),
		# 	'email':forms.EmailInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'name@gmail.com'}),
		# 	'password':forms.PasswordInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'Password'}),
		# 	'confirm_password':forms.PasswordInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'Confirm Password'}),
		# }

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)		
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
		self.fields['email'].validators.append(UniqueEmail)

	def clean(self):
		super(SignUpForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
		return self.cleaned_data


class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'Username'}), required=True,)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'floatingInput','placeholder':'Password'}), required=True)

	class Meta:
		fields = ['username', 'password']


