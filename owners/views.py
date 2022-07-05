import json

from django.views import View
from django.http import JsonResponse

from owners.models import Owner, Dog

class OwnerView(View):
    def post(self, request):
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

class DogView(View):
    def post(self, request):
        # 생성
        data = json.loads(request.body)
        owner1 = Owner.objects.get(name=data['owner_name'])
        
        Dog.objects.create(
            name = data['name'],
            age = data['age'],
            owner = owner1
        )
        return JsonResponse({'Message':'Dog created'}, status=201)
    
    def get(self, request):
        dogs = Dog.objects.all()  
        results = []
        for dog in dogs:
            results.append({
                'dog_name' : dog.name,
                'dog_age' : dog.age,
                'owner_name' : dog.owner.name
            })
        return JsonResponse({'Results':results}, status=200)