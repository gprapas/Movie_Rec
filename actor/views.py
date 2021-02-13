from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.template import loader
from django.http import HttpResponse

from actor.models import Actor
from rec.models import Movie



def actors_info(request, actor_slug):
	actor = get_object_or_404(Actor, slug=actor_slug)
	movies = Movie.objects.filter(Actors=actor)

	
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_info = paginator.get_page(page_number)

	data = {
		'movie_info': movie_info,
		'actor': actor,
	}


	template = loader.get_template('actor_info.html')

	return HttpResponse(template.render(data, request))