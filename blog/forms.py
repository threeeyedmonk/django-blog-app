from django import forms
from django.contrib.auth.models import User
from blog.models import Post, UserProfile, CommentsTable

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-input-style',
            'placeholder': 'First Name',
        }
    ), label = '')
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-input-style',
            'placeholder': 'Last Name'
        }
    ), label = '')
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-input-style',
            'placeholder': 'Username',
        }
    ), label = '')
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-input-style',
            'placeholder': 'email',
        }
    ), label = '')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-input-style',
            'placeholder': 'Password',
        }
    ), label = '')
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-input-style',
            'placeholder': 'Confirm Password',
        }
    ), label = '')
    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class UserProfileForm(forms.ModelForm):
    website = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': 'form-input-style',
            'placeholder': 'Website URL'
        }
    ), label = '')
    city = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class': 'form-input-style',
            'placeholder': 'City',
        }
    ), label = '')
    country = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class': 'form-input-style',
            'placeholder': 'Country',
        }
    ), label = '')
    class Meta():
        model = UserProfile
        fields = ['website', 'city', 'country', 'profile_image']

    def check_confirm_password(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('confirm_password')
        if not (pwd1 and pwd2):
            raise forms.ValidationError("You must confirm your password.")
        elif pwd1 != pwd2:
            raise forms.ValidationError("Passwords do not match.")
        return pwd1


class CreatePostForm(forms.ModelForm):
    post_title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control form-text',
            'placeholder': 'Enter Title Here...'
        }
    ))
    class Meta():
        model = Post
        fields = ['post_title', 'post_text']

class AddCommentForm(forms.ModelForm):
    comment_text = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter your comment here...',
        }
    ), label = '')
    class Meta():
        model = CommentsTable
        fields = ['comment_text']

class UpdateDraftForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ['post_title', 'post_text']
