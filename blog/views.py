from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import UserForm, UserProfileForm, CreatePostForm, AddCommentForm
from blog.models import Post, UserProfile
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView

from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#@login_required

class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/editpost.html'
    fields = ['post_title', 'post_text']


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
    ordering = ['-post_published']

#class PostDetailView(LoginRequiredMixin, DetailView):
#    '''
#    Displays post in a detailed view
#    '''
#    context_object_name = "post_detail"
#    model = Post
#    template_name = 'blog/postdetail.html'

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
            if 'draft' in request.POST:
                new_form.draft_state = True
                new_form.save()
                return HttpResponse("Saved in Draft!")
                return redirect('blog:showdrafts')
            new_form.post_published = timezone.now()
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
        #print(str(uname) + '-' + str(pwd))

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

def addcomment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    users = User.objects.all()

    if request.method == "POST":
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = request.user
            comment.post_title = post
            comment.save()
            return redirect('blog:postdetail', pk=post.pk)
    else:
        form = AddCommentForm()
    return render(request, 'blog/postdetail.html', {'form': form,
                                                    'post_detail': post,
                                                    'users': users})


class ShowDraftsListView(LoginRequiredMixin, ListView):
    context_object_name = 'userprofile'
    model = UserProfile
    template_name = 'blog/showdrafts.html'

class ShowPostsListView(LoginRequiredMixin, ListView):
    context_object_name = 'userprofile'
    model = UserProfile
    template_name = 'blog/showposts.html'


def deletepost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        if 'yes' in request.POST:
            post.delete()
            messages.success(request, "Request post has been deleted.")
            return redirect('blog:userprofile')
        elif 'no' in request.POST:
            return redirect('blog:userprofile')

    return render(request, 'blog/deletepost.html', {'post': post})
