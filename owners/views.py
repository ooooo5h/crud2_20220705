import json

from django.views import View
from django.http import JsonResponse

from owners.models import Owner, Dog

class OwnerView(View):
    """
    목적 : 주인의 정보를 데이터베이스에 저장
    
    1. client로부터 받아야하는 정보
        - 이름
        - 이메일
        - 나이
    2. 받은 정보를 ORM을 이용해서 저장
    """
    def post(self, request):
        data = json.loads(request.body)
        Owner.objects.create(
            name  = data['name'],
            email = data['email'],
            age   = data['age']
        )
        return JsonResponse({'Message':'Owner created'}, status=201)

    def get(self, request):
        owners = Owner.objects.all()
        result = []
        for owner in owners:
            dogs = owner.dog_set.all()  # Dog.objects.filter(owner=owner) 필터를 걸어서 가져와도 쿼리셋/, 역참조로 all을 해도 쿼리셋인데 
            # 깡아지 입장에서 owner는 정참조다.
            # 주인 입장에서 강아지 정보는 없다. 없지만 강아지가 
            # 주인과관계가 있기 때문에 주인도 강아지의 정보를 가져올 수 있다.
            # 이게 역참조!!! 속성.으로 가면 정참고, .으로 접근 못하지만 관계가 걸려있는 데이터를 가져올때는 역참조
            # 역참조 관계가 되면 데이터를 여러개 가져올 수 잇다..?
            # 역참조로 가져오면 그치그치 읻래다의 관계에서 다대 1일이잠,ㄴ 1의 관계에서는 다니까.
            # 역참조를 위한 매니저클래스가 클래스이름_set이다. objects와 같은 매니저클래스.
            # set을 적기 싫으면 related_name을 적어주면 된다. 저걸 dogs로 하면 
            # owner의 역참조 이름이 related_name을 적어주면
            # 그 이름이 역참조를 ㅎ기 위핸 매니저클래스의 이름이 된다.!!
            # 클래스이름_set이싫다면 저렇게 해줄 수 있다.
            
            dog_list = []
            for dog in dogs:
                dog_list.append({
                    'dog_name' : dog.name,
                    'dog_age'  : dog.age,
                })
            result.append({
                'name'  : owner.name,
                'email' : owner.email,
                'age'   : owner.age,
                'dogs'  : dog_list
            })
        return JsonResponse({'result':result}, status=200)

class DogView(View):
    """
    목적 : 강아지의 정보를 데이터베이스에 저장
    
    1. client로부터 받아야하는 정보
        - 강아지 이름
        - 강아지 나이
        - 주인의 정보
    2. 받은 정보를 ORM을 이용해서 저장
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # 멘토님은 클라이언트가 보낸 데이터 검증을 먼저 실시한다.
            # 키 에러가 발생하면 바로 끝나도록!
            owner_id = data['owner']
            name     = data['name']
            age      = data['age']            
            
            # if not Owner.objects.filter(id=owner_id).exists():
            #     # 예외처리의 두번째 방법 : if문으로 !! 
            #     # exitsts는 없으면 false가 리턴된다.
            #     # 존재한다면 여기로 안들어옴.
            #     return JsonResponse({'Message':'Not Found'}, status=404)

            owner = Owner.objects.get(id=owner_id)  
            # get은 무조건 한가지만 가져온다. 그렇기때문에 name으로 가져오면
            # 값이 2개 이상일 경우 multi~~저쩌고 에러가 발생한다.
            # pk 유일한 값을 가지고 조회하는 게 좋다!
        
            Dog.objects.create(
                name  = name,
                age   = age,
                owner = owner
            )
            return JsonResponse({'Message':'Dog created'}, status=201)
        # 없는 owner의 id값을 넣었을 때 발생하는 처리
        except Owner.DoesNotExist:
            return JsonResponse({'Message':'Not Found'}, status=404)
        # 키에러 처리 => owner로 클라이언트가 요청을 보낸게 아니라 owner_id로 보냈다던가 그럴 때 발생하는 처리!!
        except KeyError:
            return JsonResponse({'Message':'Key Error'}, status=400)
    
    def get(self, request):
        """
        목적 : 강아지의 정보를 데이터베이스로부터 가져와서 전달
        
        1. 데이터베이스에서 강아지의 정보를 전부 가져온다.
        2. 가져온 데이터를 json으로 보낼 수 있도록 가공한다.(객체를 딕셔너리로 바꾸는 방법)
        3. 가공한 데이터를 전달한다.
        """
        dogs = Dog.objects.all()  
        result = []
        for dog in dogs:
            result.append({
                'dog_name'   : dog.name,
                'dog_age'    : dog.age,
                'owner_name' : dog.owner.name   
                # dog클래스에 owner라는 속성이 있고, 
                # fk키로 연결이 되어있고
                # Owner을 가리킨다.
                # .을 찍으면 Owner 클래스의 속성을 사용할 수 있다.
            })
        return JsonResponse({'Result':result}, status=200)