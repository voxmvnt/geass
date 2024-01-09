from django.shortcuts import render
from blog.models import Post
from django.db.models import Count

def main(request):
    like_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    recent_posts = Post.objects.order_by('-pk')[:5]
    context = {
        'like_posts': like_posts,
        'recent_posts': recent_posts,
    }
    return render(request, "single_pages/main.html", context)

def about_engineer(request):
    return render(request, "single_pages/about_engineer.html")

def login(request):
    return render(request, "single_pages/login.html")