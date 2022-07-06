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
            dogs = owner.dog_set.all()  
                        
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
            })
        return JsonResponse({'Result':result}, status=200)