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
    
    def get(self, request):
        owners = Owner.objects.all()
        result = []
        for owner in owners:
            result.append({
                'name' : owner.name,
                'email' : owner.email,
                'age' : owner.age
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
