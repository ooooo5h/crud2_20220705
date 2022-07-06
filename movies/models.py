from django.db import models

class Actor(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    date_of_birth = models.DateField()
    movies = models.ManyToManyField('Movie', through='ActorAndMovie')
    
    class Meta:
        db_table = 'actors'
        
        
class Movie(models.Model):
    title = models.CharField(max_length=45)
    release_date = models.DateField()
    running_time = models.IntegerField()
    
    class Meta:
        db_table = 'movies'
        
class ActorAndMovie(models.Model):
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'actors_movies'