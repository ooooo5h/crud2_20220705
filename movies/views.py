import json

from django.http import JsonResponse
from django.views import View

from movies.models import Actor, Movie, ActorAndMovie

class ActorView(View):
    def post(self, request):
        data = json.loads(request.body)
        Actor.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            date_of_birth = data['date_of_birth']
        )
        
        return JsonResponse({'Request':'Actor created'}, status=201)
    

    def get(self, request):
        actors = Actor.objects.all()
        results = []
        
        for actor in actors:    
            movies = actor.movies.all()
            movie_list = []
            for movie in movies:
                movie_list.append(movie.title)
                
            results.append({
                'last_name' : actor.last_name,
                'first_name' : actor.first_name,
                'movies' : movie_list
            })
        return JsonResponse({'Results':results}, status=200)
    
class MovieView(View):
    def post(self, request):
        data = json.loads(request.body)
        Movie.objects.create(
            title = data['title'],
            release_date = data['release_date'],
            running_time = data['running_time']
        )
        
        return JsonResponse({'Request':'Movie created'}, status=201)
    
    def get(self, request):
        movies = Movie.objects.all()   
        results = []
        for movie in movies:
            actors = movie.actor_set.all()
            actors_list = []
            
            for actor in actors:
                actors_list.append({
                    'actor_first_name' : actor.first_name,  # actor_and_movie객체에는 actor라는 외래키가 있으니까 . 타고 이동이 가능하다
                    'actor_last_name' : actor.last_name,
                })
            
            results.append({
                'title' : movie.title,
                'running_time' : movie.running_time,
                'actors' : actors_list,
            })
        
        return JsonResponse({'Results':results}, status=200)
    
class ActorAndMovieView(View):
    def post(self, request):
        data = json.loads(request.body)
        ActorAndMovie.objects.create(
            actor_id = data['actor_id'],
            movie_id = data['movie_id']
        )
        
        return JsonResponse({'Request':'Actor and Movie created'}, status=201)

        
    
