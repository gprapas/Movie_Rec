from django.urls import path
from actor.views import actors_info


urlpatterns = [
	path('<slug:actor_slug>', actors_info, name='actors'),
]