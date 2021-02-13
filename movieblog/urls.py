from django.urls import path
from .views import movie_blog, Article_Info

urlpatterns = [ 
   
    path('', movie_blog.as_view(), name = 'movie_blog'),
    path('article/<int:pk>', Article_Info.as_view(), name='article_info')
    
]