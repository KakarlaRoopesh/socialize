
from django.core.exceptions import ImproperlyConfigured
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from .forms import CreateNewUser
from django.contrib.auth import authenticate,login,logout
from .models import UserProfile,Follow 
from django.contrib.auth.forms import AuthenticationForm
from .forms import EditProfile
from django.contrib.auth.decorators import login_required
from post.forms import PostForm
from django.contrib.auth.models import User

# Create your views here.


def sign_up(request):

    form = CreateNewUser
    registered= False
    if request.method == 'POST':
        form = CreateNewUser(data = request.POST)
        if form.is_valid():
            user = form.save()
            registered= True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return redirect('app_login:login')
    context = {'form':form}
    return render(request,'app_login/sign_up.html',context)         


    





def login_page(request):
    form = AuthenticationForm
    if request.method == 'POST':
        form= AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('app_post:home')
    context={
        'form':form
    }            
    return render(request,'app_login/login.html',context)                       


@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST,request.FILES,instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)


    context = {
        'form':form
    }
    return render(request,'app_login/profile.html',context)
    
        
@login_required     
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('app_login:login'))


@login_required
def profile(request):
    form = PostForm
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('app_post:home'))
    context = {'form':form}
    return render(request,'app_login/user.html',context)    



@login_required
def user(request,username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user,following = user_other)
    if user == request.user:
        return HttpResponseRedirect(reverse('app_login:profile'))
    context={
        'user_other':user_other,
        'already_followed':already_followed
    }
    return render(request,'app_login/user_other.html',context)


@login_required
def follow(request,username):
    following_user = User.objects.get(username=username)
    follower_user = request.user 
    already_followed = Follow.objects.filter(follower=follower_user,following = following_user)
    if not already_followed:
        followed_user = Follow(follower=follower_user,following = following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('app_login:user',kwargs={'username': username }))


@login_required
def unfollow(request,username):
    following_user = User.objects.get(username=username)
    follower_user = request.user 
    already_followed = Follow.objects.filter(follower=follower_user,following = following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('app_login:user',kwargs={'username': username }))


