from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include
from authent.views import UserProfile, UserProfileWatchList, UserProfileMoviesLiked, ReviewDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rec/', include('rec.urls')),
    path('blog/',include('movieblog.urls')),
    path('', include('authent.urls')),
    path('actors/', include('actor.urls')),
    path('<username>/', UserProfile, name='profile'),
    path('<username>/watchlist', UserProfileWatchList, name='profile-watch-list'),
    path('<username>/likedlist', UserProfileMoviesLiked, name='profile-liked-list'),      
    path('<username>/review/<imdb_id>', ReviewDetail, name='user-review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
