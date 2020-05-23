from django.shortcuts import render, redirect
from blog.forms import RegisterForm, CreatePostForm
from blog.models import Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#@login_required
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
    form = RegisterForm

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('blog:home')
        else:
            print("ERROR: Invalid Form")
    else:
        return render(request, 'blog/register.html', {'form': form})

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
