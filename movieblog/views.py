from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post



class movie_blog(ListView):
    model = Post
    template_name = 'movie_blog.html' 
    
    
    
    
    
    
class Article_Info(DetailView):
    model = Post
    template_name = 'article_info.html'