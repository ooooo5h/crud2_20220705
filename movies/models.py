from django.db import models

class Actor(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    date_of_birth = models.DateField()
    # 속성이 들어와야한다. 장고에서 mtm필드를 생서하면 
    # through속성이 없이 관계테이블도 없다면 장고가 자동으로 만든다.
    # 단점은 내가 만든게 아니라 장고가 만든테이블이기때문에 관리하기 어려움이 있을 수 있다.
    # through는 내가 만든 테이블을 중간테이블로 쓸꺼야하고 정의해주는 속성
    
    #manytomany를 사용하면 actor의 movies를 통해서 접근하거, movie에서 ator을 찾을때 역참조처럼 사용이 가능하다.
    
    # 액터안에 생성한 movies속성은 db에 생성되지 않는다. 로직할때만 이용된다.
    # 매니저 클래스가 된다.
    
    class Meta:
        db_table = 'actors'
        
    def __str__(self):
        return self.first_name
        
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