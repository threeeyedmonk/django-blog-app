from django.shortcuts import render, redirect
from blog.forms import UserForm, UserProfileForm, CreatePostForm
from blog.models import Post, UserProfile
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#@login_required

class UserProfileView(LoginRequiredMixin, DetailView):
    '''
    Displays logged in user's profile_image
    '''
    context_object_name = 'userprofile'
    model = UserProfile
    template_name = 'blog/userprofile.html'

    def get_object(self):
        return self.request.user

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    ordering = ['-post_created']

class PostDetailView(LoginRequiredMixin, DetailView):
    '''
    Displays post in a detailed view
    '''
    context_object_name = "post_detail"
    model = Post
    template_name = 'blog/postdetail.html'

@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:home'))

@login_required
def createpost(request):
    form = CreatePostForm

    if request.method == "POST":
        form = CreatePostForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            print(request.user)
            new_form.author = request.user
            new_form.save()
            return redirect('blog:home')
        else:
            print("ERROR: INVALID SAVE")
    else:
        return render(request, 'blog/createpost.html', {'form': form})


def register(request):

    if request.method == 'POST':
        userform = UserForm(data=request.POST)
        userprofileform = UserProfileForm(data=request.POST)

        if userform.is_valid() and userprofileform.is_valid():
            user = userform.save(commit=False)
            user.set_password(userform.cleaned_data['password'])
            user.save()
            profile = userprofileform.save(commit=False)
            profile.user = user
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            profile.save()

            return redirect('blog:home')
        else:
            print("ERROR: Invalid Form")
    else:
        userform = UserForm()
        userprofileform = UserProfileForm()

    return render(request, 'blog/register.html', {'userform': userform,
                                                    'userprofileform': userprofileform})

def userlogin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        print(str(uname) + '-' + str(pwd))

        user = authenticate(username=uname, password=pwd)

        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse('blog:home'))
        else:
            return HttpResponse("Incorrect username/password. Please try again!")

    else:
        return render(request, 'blog/login.html', {})
