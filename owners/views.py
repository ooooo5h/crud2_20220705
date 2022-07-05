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

## 외래키인 아이들은 xx_id 붙여야 가져온다.
class DogView(View):
    def post(self, request):
        # 생성
        data = json.loads(request.body)
        
        Dog.objects.create(
            name = data['name'],
            age = data['age'],
            owner_id = data['owner_id']   # owner_id로 바꿔야한다. fk인 아이들은 xxxx_id로 넣어줄 수 있다.
        )
        return JsonResponse({'Message':'Dog created'}, status=201)
