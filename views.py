from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app_login.models import UserProfile,Follow
from post.models import Post,Like

from django.urls import reverse

# Create your views here.

@login_required
def home(request):
    following_list = Follow.objects.filter(follower = request.user)
    posts = Post.objects.filter(author__in=following_list.values_list('following'))
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list=liked_post.values_list('post',flat=True)
    if request.method == 'GET':
        search = request.GET.get('search','')
        result = User.objects.filter(username__icontains=search)

    context = {
        'search':search,
        'result':result,
        'posts':posts,
        'liked_post_list':liked_post_list
        }    
    return render(request,'post/home.html',context)

@login_required
def  liked(request,pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post ,user=request.user)
    if not already_liked:
        liked_post = Like(post=post ,user=request.user)
        liked_post.save()
    return HttpResponseRedirect(reverse('app_post:home'))


@login_required
def  unliked(request,pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post ,user=request.user)
    already_liked.delete()
    
    return HttpResponseRedirect(reverse('app_post:home'))