from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Plant
# Create your views here.


# HOME PAGE 
def home_page(request: HttpRequest):

    #getting the Query Parameters
    print(request.GET)
    plants=Plant.objects.all()
    #limiting the result using slicing
    plants = Plant.objects.all().order_by('-created_at')[0:3]

    return render(request, "main/home_page.html", {"plants" : plants})



# DISPLAY ALL PLANTS 
def all_plants(request: HttpRequest):

    
    if "cat" in request.GET:
        plants = Plant.objects.filter(category=request.GET["cat"])
    else:
        plants = Plant.objects.all()

    return render(request, "main/all_plants.html", {"posts" : plants, "categories" : Plant.categories.choices})



# ADD PLANT 
def add_plant(request: HttpRequest):

    if request.method == 'POST':
        try:
            new_post = Plant(name =request.POST["name"] , about=request.POST["about"] , used_for=request.POST("used_for") , image= request.FILES["image"] ,  is_edible=request.POST["is_edible"] ,  created_at=request.POST["created_at"])
            new_post.save()
            return redirect("main:home_page")
        except Exception as e:
            print(e)

    return render(request, "main/add_plant.html", {"categories" : Plant.categories.choices})



# PLANTS DETAELS 
def plant_detail(request:HttpRequest, plant_id):

    try:
        plant = Plant.objects.get(pk=plant_id)
    except Plant.DoesNotExist:
        return render(request, "main/not_found.html")
    except Exception as e:
        print(e)

    return render(request, "main/plant_detail.html", {"plant" : plant})




# UPDATE PLANT
def update_plant(request:HttpRequest, plant_id):

    plant = Plant.objects.get(pk=plant_id)

    if request.method == "POST":
        try:
            plant.name = request.POST["name"]
            plant.about = request.POST["about"]
            plant.used_for = request.POST("used_for")
            plant.image = request.FILES("image", plant.image)
            plant.category = request.POST["category"]
            plant.is_edible = request.POST["is_edible"]
            plant.created_at = request.POST["created_at"]
            plant.save()
            return redirect("main:plant_detail_view", plant_id=plant.id)
        except Exception as e:
            print(e)

    return render(request, 'main/update_plant.html', {"post" : plant, "categories" : Plant.categories.choices})



# DELETE PLANT 
def delete_plant(request:HttpRequest, plant_id):

    try:
        plant = Plant.objects.get(pk=plant_id)
        plant.delete()
    except Exception as e:
        print(e)
    
    return redirect("main:home_page")



# ALL PLANTS SEARCH 
def all_search(request: HttpRequest):
    if request.method == 'GET':
        category = request.GET.get('category', '')

        if category:
            plants = Plant.objects.filter(category=category)
        else:
            plants = Plant.objects.all()
        return render(request, 'main/all_search.html', {'plants': plants, 'category': category})

    return HttpResponse('Invalid request')



# PLANTS SEARCH 
def plant_search(request: HttpRequest):
    if request.method == 'GET':
        category = request.GET.get('category', '')

        if category:
            plants = Plant.objects.filter(category=category)
        else:
            plants = Plant.objects.all()
        return render(request, 'main/plant_search.html', {'plants': plants, 'category': category})

    return HttpResponse('Invalid request')


