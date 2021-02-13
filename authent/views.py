from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from authent.models import Profile
from rec.models import Movie, Review 

from comments.models import chat
from comments.forms import chatForm


from authent.forms import SignupForm, EditProfileForm



from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator



    
    
    
    
def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
			return redirect('login')
	else:
		form = SignupForm()

	data = {
		'form': form,
	}

	return render(request, 'registration/signup.html', data)






@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('index')
	else:
		form = EditProfileForm()

	data = {
		'form': form,
	}

	return render(request, 'edit_profile.html', data)

@login_required
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	
	mWatched_count = profile.watched.filter(Type='movie').count()
	watch_list_count = profile.to_watch.all().count()
	m_reviewd_count = Review.objects.filter(user=user).count()


	data = {
		'profile': profile,
		'mWatched_count': mWatched_count,
		'watch_list_count': watch_list_count,
		'm_reviewd_count': m_reviewd_count,
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(data, request))
@login_required
def UserProfileWatchList(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	
	mWatched_count = profile.watched.filter(Type='movie').count()
	watch_list_count = profile.to_watch.all().count()
	m_reviewd_count = Review.objects.filter(user=user).count()

	movies = profile.to_watch.all()
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_info = paginator.get_page(page_number)


	data = {
		'profile': profile,
		'mWatched_count': mWatched_count,
		'watch_list_count': watch_list_count,
		'm_reviewd_count': m_reviewd_count,
		'movie_info': movie_info,
		'list_title': 'Watch list',
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(data, request))



@login_required
def UserProfileMoviesLiked(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	
	mWatched_count = profile.watched.filter(Type='movie').count()
	watch_list_count = profile.to_watch.all().count()
	m_reviewd_count = Review.objects.filter(user=user).count()


	movies = profile.watched.filter(Type='movie')
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_info = paginator.get_page(page_number)


	data = {
		'profile': profile,
		'mWatched_count': mWatched_count,
		'watch_list_count': watch_list_count,
		'm_reviewd_count': m_reviewd_count,
		'movie_info': movie_info,
		'list_title': 'Movies Liked',
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(data, request))
@login_required
def UserProfileMoviesReviewed(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	
	mWatched_count = profile.watched.filter(Type='movie').count()
	
	watch_list_count = profile.to_watch.all().count()
	m_reviewd_count = Review.objects.filter(user=user).count()

	
	movies = Review.objects.filter(user=user)
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_info = paginator.get_page(page_number)


	data = {
		'profile': profile,
		'mWatched_count': mWatched_count,
		
		'watch_list_count': watch_list_count,
		'm_reviewd_count': m_reviewd_count,
		'movie_info': movie_info,
		'list_title': 'Reviewed',
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(data, request))
@login_required
def ReviewDetail(request, username, imdb_id):
	user_comment = request.user
	user = get_object_or_404(User, username=username)
	movie = Movie.objects.get(imdbID=imdb_id)
	review = Review.objects.get(user=user, movie=movie)

    
	comments = chat.objects.filter(review=review).order_by('date')

	if request.method == 'POST':
		form = chatForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.review = review
			comment.user = user_comment
			comment.save()
			return HttpResponseRedirect(reverse('user-review', args=[username, imdb_id]))
	else:
		form = chatForm()
	

	data = {
		'review': review,
		'movie': movie,
        'comments': comments,
		'form': form,
		
	}

	template = loader.get_template('movie_review.html')

	return HttpResponse(template.render(data, request))
