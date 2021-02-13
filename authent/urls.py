from django.urls import path

from authent.views import Signup, EditProfile
from django.contrib.auth import views as authViews


urlpatterns = [
	path('profile/edit', EditProfile, name='edit-profile'),
	path('signup/', Signup, name='signup'),
	path('', authViews.LoginView.as_view(template_name='registration/login.html'), name='login'),
	path('logout/', authViews.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),

]