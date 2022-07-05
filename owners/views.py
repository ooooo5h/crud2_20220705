import json

from django.views import View
from django.http import JsonResponse

from owners.models import Owner, Dog

class OwnerView(View):
    def post(self, request):
        # 생성
        data = json.loads(request.body)
        Owner.objects.create(
            name=data['name'],
            email=data['email'],
            age=data['age']
        )
        return JsonResponse({'Message':'Owner created'}, status=201)
    
    # way1 
    # def get(self, request):
    #     owners = Owner.objects.all()
    #     dogs = Dog.objects.all()
    #     result = []
    #     for owner in owners:
    #         for dog in dogs:
    #             if dog.owner_id == owner.id:
    #                 result.append({
    #                     'name' : owner.name,
    #                     'email' : owner.email,
    #                     'age' : owner.age,
    #                     'dog_name' : dog.name,
    #                     'dog_age' : dog.age,
    #                 })
        
    #     return JsonResponse({'results':result}, status=200)
    
    # way2
    def get(self, request):
        owners = Owner.objects.all()
        result = []
        for owner in owners:
            dogs = Dog.objects.filter(owner_id=owner.id)
            dog_list = []
            for dog in dogs:
                dog_list.append({
                    'dog_name' : dog.name,
                    'dog_age' : dog.age,
                })
            result.append({
                'name' : owner.name,
                'email' : owner.email,
                'age' : owner.age,
                'dogs' : dog_list
            })
        return JsonResponse({'results':result}, status=200)

    

# 에러 발생...ㅠㅠㅠ
# class DogView(View):
#     def post(self, request):
#         # 생성
#         data = json.loads(request.body)
        
#         Dog.objects.create(
#             name = data['name'],
#             age = data['age'],
#             owner = data['owner_id']   # 에러발생 ValueError: Cannot assign "'1'": "Dog.owner" must be a "Owner" instance.
#         )
#         return JsonResponse({'Message':'Dog created'}, status=201)

# id가 아닌 이름으로 post하는 방법
class DogView(View):
    def post(self, request):
        # 생성
        data = json.loads(request.body)
        owner1 = Owner.objects.get(name=data['owner_name'])
        # 클라이언트가 보낸 request의 body부분 중 키값이 owner_name인 벨류값을 갖고와서
        # owner의 객체들 중에 일치하는 객체 1개만 갖고와 
        
        Dog.objects.create(
            name = data['name'],
            age = data['age'],
            owner = owner1
        )
        return JsonResponse({'Message':'Dog created'}, status=201)

    ## 복잡하게 짤 필요가 없었어!! 에러 발생
    # AttributeError: type object 'Dog' has no attribute 'owner_set'
    # def get(self, request):
    #     # 조회
    #     dogs = Dog.objects.all()
    #     results = []
    #     for dog in dogs:
    #         dog_owner = Dog.owner_set.get(id=dog.owner_id)
    #         results.append({
    #             'dog_name' : dog.name,
    #             'dog_age' : dog.age,
    #             'owner_name' : dog_owner.name
    #         })
    #     return JsonResponse({'Results':results}, status=200)
    
    def get(self, request):
        dogs = Dog.objects.all()  # dogs에는 querySet이 담겨있다 하나하나씩 쪼개서 담아줘야한다
        results = []
        for dog in dogs:
            results.append({
                'dog_name' : dog.name,
                'dog_age' : dog.age,
                'owner_name' : dog.owner.name
            })
        return JsonResponse({'Results':results}, status=200)