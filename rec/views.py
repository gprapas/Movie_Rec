from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from rec.forms import RateForm
import requests
from actor.models import Actor
from django.utils.text import slugify
from django.db.models import Avg
from django.urls import reverse
from django.contrib import messages
from authent.models import Profile
from rec.models import Movie, Genre, Rating, Review
from django.core.paginator import Paginator
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
from ast import literal_eval
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity



df1=pd.read_csv('C:/Users/eglav/Documents/diplwmatiki/Movie_Recommendations/Movie_recommendations/tmdb_5000_credits.csv')
df2=pd.read_csv('C:/Users/eglav/Documents/diplwmatiki/Movie_Recommendations/Movie_recommendations/tmdb_5000_movies.csv')


df1.columns = ['id','tittle','cast','crew']
df2 = df2.merge(df1,on='id')
df2['tittle'] =  df2['tittle'].str.lower()


tfidf = TfidfVectorizer(stop_words='english')


df2['overview'] = df2['overview'].fillna('')


tfidf_matrix = tfidf.fit_transform(df2['overview'])

tfidf_matrix.shape


cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()


features = ['cast', 'crew', 'keywords', 'genres','production_companies']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)
    

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        
        if len(names) > 3:
            names = names[:3]
        return names

    return []

df2['director'] = df2['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres','production_companies']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)
    
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

features = ['cast', 'keywords', 'director', 'genres', 'production_companies']

for feature in features:
    df2[feature] = df2[feature].apply(clean_data)
    
def create_the_mix(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres']) + ' ' + ''.join(x['production_companies'])
df2['mix'] = df2.apply(create_the_mix, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['mix'])


cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])

def get_recommendations(title, cosine_sim=cosine_sim):
   
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))


    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

   
    sim_scores = sim_scores[1:11]

   
    movie_indices = [i[0] for i in sim_scores]

    t = 0
    for val in df2['title'].iloc[movie_indices] :
        
        if (t==0):
            prwti = val
        elif (t==1):
            deuteri = val
        elif (t==2):
            triti = val
        elif (t==3):
            tetarti = val
        elif (t==4):
            pemti = val
        elif (t==5):
            ekti = val
        elif(t==6):
            evdomi = val
        elif(t==7):
            ogdoi = val
        elif(t==8):
            enati = val
        else:
            dekati = val
        t = t + 1
    
    str1 = prwti + '\n' + deuteri + '\n' + triti + '\n' + tetarti + '\n' + pemti + '\n' + ekti + '\n' + evdomi + '\n' + ogdoi + '\n' + enati + '\n' + dekati               
    return str1




def index(request):
	query = request.GET.get('q')

	if query:
		url = 'http://www.omdbapi.com/?apikey=d4a899e2&s=' + query
		response = requests.get(url)
		movie_info = response.json()
    
    

		data = {
			'query' : query,
			'movie_info' : movie_info,
			'page_number': 1,
            
		}
		template = loader.get_template('search_result.html')
		return HttpResponse(template.render(data, request))

	return render(request, 'index.html')


def checkTitle(title):
    k=0
    
    
    if df2['tittle'].str.contains(title).any():
        k=0
    else:
        k=1
    return k 

    
def recommendations (request):
        
        
        query = request.GET.get('q')
        query = str(query).lower()
        
        if query:
            check = checkTitle(query)
            
    
            if check==1:    
               messages.error(request, ' ')
            else:
              
                query = query.title()
                
                
               
                        
                txt = get_recommendations(query,cosine_sim2)
                data1 = txt.split("\n")
                i=0
                for movie in data1:
                    if (i==0):            
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info = response.json()
                    elif (i==1):
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info1 = response.json()
                    elif (i==2):
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info2 = response.json()
                    elif (i==3):
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info3 = response.json()
                    elif (i==4):
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info4 = response.json()
                    elif (i==5):
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info5 = response.json()
                    elif (i==6):
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info6 = response.json()
                    elif (i==7):
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info7 = response.json()
                    elif (i==8):
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info8 = response.json()
                    else:
                        url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + movie
                        response = requests.get(url)
                        movie_info9 = response.json()
                    i = i+1
                        
              
                   
                data = {
        			'query' : query,
                    'movie_info' : movie_info,
                    'movie_info1' : movie_info1,
                    'movie_info2' : movie_info2,
                    'movie_info3' : movie_info3,
                    'movie_info4' : movie_info4,
                    'movie_info5' : movie_info5,
                    'movie_info6' : movie_info6,
                    'movie_info7' : movie_info7,
                    'movie_info8' : movie_info8,
                    'movie_info9' : movie_info9,
        			'page_number': 1,
                    
        
        		}
                template = loader.get_template('recommendation_result.html')
                return HttpResponse(template.render(data, request))
        
        
        
        
        
        
            
            
        return render(request, 'recommendations.html')



def movieInformation(request, imdb_id):

	if Movie.objects.filter(imdbID=imdb_id).exists():
		movie_info = Movie.objects.get(imdbID=imdb_id)
		reviews = Review.objects.filter(movie=movie_info)
		reviews_avg = reviews.aggregate(Avg('rate'))
		reviews_count = reviews.count()
		our_db = True

		data = {
			'movie_info': movie_info,
			'reviews': reviews,
			'reviews_avg': reviews_avg,
			'reviews_count': reviews_count,
			'our_db': our_db,
		}

	else:
		url = 'http://www.omdbapi.com/?apikey=d4a899e2&i=' + imdb_id
		response = requests.get(url)
		movie_info = response.json()

	

		rating_objs = []
		genre_objs = []
		actor_objs = []

	
		actor_list = [x.strip() for x in movie_info['Actors'].split(',')]

		for actor in actor_list:
			a, created = Actor.objects.get_or_create(name=actor)
			actor_objs.append(a)

	
		genre_list = list(movie_info['Genre'].replace(" ", "").split(','))

		for genre in genre_list:
			genre_slug = slugify(genre)
			g, created = Genre.objects.get_or_create(title=genre, slug=genre_slug)
			genre_objs.append(g)

		
		for rate in movie_info['Ratings']:
			r, created = Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
			rating_objs.append(r)
       
		if movie_info['Type'] == 'movie':
			m, created = Movie.objects.get_or_create(
				Title=movie_info['Title'],
				Year=movie_info['Year'],
				Rated=movie_info['Rated'],
				Released=movie_info['Released'],
				Runtime=movie_info['Runtime'],
				Director=movie_info['Director'],
				Writer=movie_info['Writer'],
				Plot=movie_info['Plot'],
				Language=movie_info['Language'],
				Country=movie_info['Country'],
				Awards=movie_info['Awards'],
				Poster_url=movie_info['Poster'],
				Metascore=movie_info['Metascore'],
				imdbRating=movie_info['imdbRating'],
				imdbVotes=movie_info['imdbVotes'],
				imdbID=movie_info['imdbID'],
				Type=movie_info['Type'],
				DVD=movie_info['DVD'],
				BoxOffice=movie_info['BoxOffice'],
				Production=movie_info['Production'],
				Website=movie_info['Website'],
				)
			m.Genre.set(genre_objs)
			m.Actors.set(actor_objs)
			m.Ratings.set(rating_objs)

		else:
			m, created = Movie.objects.get_or_create(
				Title=movie_info['Title'],
				Year=movie_info['Year'],
				Rated=movie_info['Rated'],
				Released=movie_info['Released'],
				Runtime=movie_info['Runtime'],
				Director=movie_info['Director'],
				Writer=movie_info['Writer'],
				Plot=movie_info['Plot'],
				Language=movie_info['Language'],
				Country=movie_info['Country'],
				Awards=movie_info['Awards'],
				Poster_url=movie_info['Poster'],
				Metascore=movie_info['Metascore'],
				imdbRating=movie_info['imdbRating'],
				imdbVotes=movie_info['imdbVotes'],
				imdbID=movie_info['imdbID'],
				Type=movie_info['Type'],
				totalSeasons=movie_info['totalSeasons'],
				)

			m.Genre.set(genre_objs)
			m.Actors.set(actor_objs)
			m.Ratings.set(rating_objs)


		for actor in actor_objs:
			actor.movies.add(m)
			actor.save()

		m.save()
		our_db = False

		data = {
			'movie_info': movie_info,
			'our_db': our_db,
		}

	template = loader.get_template('movie_informations.html')

	return HttpResponse(template.render(data, request))

def pagination(request, query, page_number):
	
    page_number = int(page_number) + 1
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&s=' + query + '&page=' + str(page_number)
    response = requests.get(url)
    movie_info = response.json()
	

    data = {
		'query': query,
		'movie_info': movie_info,
		'page_number': page_number,
	}

    template = loader.get_template('search_result.html')

    return HttpResponse(template.render(data, request))





def addMoviesLiked(request, imdb_id):
	movie = Movie.objects.get(imdbID=imdb_id)
	user = request.user
	profile = Profile.objects.get(user=user)

	profile.watched.add(movie)

	return HttpResponseRedirect(reverse('movie-informations', args=[imdb_id]))

def genres_movies(request, genre_slug):
	genre = get_object_or_404(Genre, slug=genre_slug)
	movies = Movie.objects.filter(Genre=genre)

	#Pagination
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_info = paginator.get_page(page_number)

	data = {
		'movie_info': movie_info,
		'genre': genre,
	}


	template = loader.get_template('genre_info.html')

	return HttpResponse(template.render(data, request))


def addMoviesToWatchList(request, imdb_id):
	movie = Movie.objects.get(imdbID=imdb_id)
	user = request.user
	profile = Profile.objects.get(user=user)

	profile.to_watch.add(movie)

	return HttpResponseRedirect(reverse('movie-informations', args=[imdb_id]))





def Rate(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user
            rate.movie = movie
            rate.save()
            return HttpResponseRedirect(reverse('movie-informations', args=[imdb_id]))
    else:
            form = RateForm()

    template = loader.get_template('rate.html')

    data = {
        'form': form, 
        'movie': movie,
    }

    return HttpResponse(template.render(data, request))




def addMoviesWatched(request, imdb_id):
	movie = Movie.objects.get(imdbID=imdb_id)
	user = request.user
	profile = Profile.objects.get(user=user)

	if profile.to_watch.filter(imdbID=imdb_id).exists():
		profile.to_watch.remove(movie)
		profile.watched.add(movie)
		
	else:
		profile.watched.add(movie)

	return HttpResponseRedirect(reverse('movie-informations', args=[imdb_id]))



def recommendationstop10(request):
    mov = 'The Shawshank Redemption'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'The Godfather'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = 'The Godfather: Part II'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = 'The Dark Knight'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = '12 Angry Men'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Schindler's List"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'The Lord of the Rings: The Return of the King'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Pulp Fiction'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'The Lord of the Rings: The Fellowship of the Ring'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = 'Fight Club'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('recommendation-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'recommendation-top10.html')





def actiontop10(request):
    mov = 'The Dark Knight'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'The Lord of the Rings: The Return of the King'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = 'Inception'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = 'The Lord of the Rings: The Fellowship of the Ring'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'The Lord of the Rings: The Two Towers'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = 'The Matrix'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Star Wars: Episode V - The Empire Strikes Back'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Star Wars'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Harakiri'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = 'Gladiator'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('action-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'action-top10.html')


def comedytop10(request):
    mov = 'Toy Story'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'La vita è bella'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Singin' in the Rain"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = 'Back to the Future'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'Modern Times'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = 'City Lights'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = '3 Idiots'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'The Great Dictator'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = 'Toy Story 3'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('comedy-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'comedy-top10.html')

def dramatop10(request):
    mov = 'The Shawshank Redemption'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'The Godfather'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "12 Angry Men"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = 'Fight Club'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'Forrest Gump'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "One Flew Over the Cuckoo's Nest"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Whiplash'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Saving Private Ryan'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'The Green Mile'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = 'The Silence of the Lambs'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('drama-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'drama-top10.html')


def scifitop10(request):
    mov = 'Avengers: Endgame'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'Interstellar'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Inception"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = 'Star Wars'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'Back to the Future'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "The Matrix"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Jurassic Park'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'The Prestige'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Mad Max: Fury Road'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = 'Star Wars: Episode VI - Return of the Jedi'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('scifi-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'scifi-top10.html')



def sporttop10(request):
    mov = 'Hoosiers'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'Rocky'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Raging Bull"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = 'Million Dollar Baby'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'The Fighter'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Rudy"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Remember the Titans'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Glory Road'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Miracle'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = 'The Karate Kid'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('sport-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'sport-top10.html')

def biographytop10(request):
    mov = 'The Sound of Music'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'The Professor and the Madman'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Hamilton"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = 'Bombshell'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'Ford v Ferrari'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Rocketman"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Bohemian Rhapsody'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Searching for Bobby Fischer'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Eddie the Eagle'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = 'The Wolf of Wall Street'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('biography-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'biography-top10.html')

def horrortop10(request):
    mov = 'Psycho'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'The Shining'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Alien"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Tumbbad"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'The Blue Elephant'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "The Thing"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'What Ever Happened to Baby Jane?'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Night of the Living Dead '
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'The Exorcist'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = "Rosemary's Baby"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('horror-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'horror-top10.html')

def musicaltop10(request):
    mov = 'The Sound of Music'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'The Wizard of Oz'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Grease"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Singin' in the Rain"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'Mary Poppins'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Mamma Mia!"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Moulin Rouge'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Annie'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'The Phantom of the Opera'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = 'West Side Story'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('musical-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'musical-top10.html')


def romancetop10(request):
    mov = 'Titanic'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'Passengers'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Midnight in Paris"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Eternal Sunshine of the Spotless Mind"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'The Princess Bride'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Before Sunrise"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Groundhog Day'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Before Sunset'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Her'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = "Silver Linings Playbook"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('romance-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'romance-top10.html')

def carstop10(request):
    mov = 'The Fast and the Furious'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'Fast Five'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Mad Max: Fury Road"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Bullitt"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = '2 Fast 2 Furious'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Death Race"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'The Italian Job'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'The Transporter'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Rush'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = "Need for Speed"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('cars-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'cars-top10.html')

def magictop10(request):
    mov = "Harry Potter and the Sorcerer's Stone"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'Harry Potter and the Chamber of Secrets'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "The Prestige"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Hugo"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'Maleficent'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Fantastic Beasts and Where to Find Them"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'The Chronicles of Narnia: The Lion, the Witch and the Wardrobe'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Now You See Me'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'The Illusionist'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = "Harry Potter and the Deathly Hallows: Part 1"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('magic-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'magic-top10.html')


def heroestop10(request):
    mov = "The Dark Knight"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'Avengers: Infinity War '
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Avengers: Endgame"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Thor: Ragnarok"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'Deadpool'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Guardians of the Galaxy"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Wonder Woman'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Logan'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Captain Marvel'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = "Black Panther"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('heroes-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'heroes-top10.html')



def christmastop10(request):
    mov = "Home Alone"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'Love Actually'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "National Lampoon's Christmas Vacation"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Elf"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'The Christmas Chronicles'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Last Christmas"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'White Christmas'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'A Christmas Story'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'The Polar Express'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = "Scrooged"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('christmas-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'christmas-top10.html')


def spytop10(request):
    mov = "From Russia with Love"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'The Bourne Ultimatum'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "Casino Royale"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Notorious"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'Skyfall'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Munich"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Mission: Impossible - Ghost Protocol'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Kingsman: The Secret Service'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Argo'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = "Bridge of Spies"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('spy-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'spy-top10.html')


def westerntop10(request):
    mov = "Django Unchained"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'The Hateful Eight'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "News of the World"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Tombstone"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'The Sons of Katie Elder'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "The Cowboys"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'The Outlaw Josey Wales'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'Bone Tomahawk'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Big Jake'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = "Chisum"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('western-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'western-top10.html')

def spacetop10(request):
    mov = "Star Wars"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info1 = response.json() 
    
    mov = 'Star Trek II: The Wrath of Khan'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info2 = response.json() 
    
    mov = "2001: A Space Odyssey"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info3 = response.json() 
    
    mov = "Star Trek"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info4 = response.json()
    
    mov = 'Star Wars: Episode III - Revenge of the Sith'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info5 = response.json()
    
    mov = "Interstellar"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info6 = response.json()
    
    mov = 'Star Wars: Episode VII - The Force Awakens'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info7 = response.json()
    
    mov = 'The Martian'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info8 = response.json()
    
    mov = 'Gravity'
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info9 = response.json()
    
    mov = "Rogue One"
    url = 'http://www.omdbapi.com/?apikey=d4a899e2&t=' + mov
    response = requests.get(url)
    movie_info10 = response.json()
    
    
    
    data = {
        'movie_info1' : movie_info1,
        'movie_info2' : movie_info2,
        'movie_info3' : movie_info3,
        'movie_info4' : movie_info4,
        'movie_info5' : movie_info5,
        'movie_info6' : movie_info6,
        'movie_info7' : movie_info7,
        'movie_info8' : movie_info8,
        'movie_info9' : movie_info9,
        'movie_info10' : movie_info10,
        			
}
    template = loader.get_template('space-top10.html')
    return HttpResponse(template.render(data, request))
    return render(request, 'space-top10.html')



