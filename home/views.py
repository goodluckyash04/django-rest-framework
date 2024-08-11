from rest_framework.response import Response
from rest_framework.decorators import api_view
from home.models import Person,Color
from .serializer import PeopleSerializer, ColorSerializer, LoginSerializer
from django.shortcuts import get_object_or_404



POST = "POST"
PUT = "PUT"
GET = "GET"
PATCH = "PATCH"
DELETE = "DELETE"



def decorator_func(func):
    def auth_check(request, *args, **kwarg):
        if request.headers.get("token") != "dqwd5s2":
            return Response("Unauthorised")
        print(func.__code__.co_varnames)
        if "us" in func.__code__.co_varnames:
            kwarg["us"] = 1
        return func(request, *args, **kwarg)

    return auth_check

@api_view([GET])
def index(request):
    return Response("Welcome to REST framework")


@api_view([POST])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)
    if not serializer.is_valid():
        return Response(serializer.errors)
          
    res_data = serializer.validated_data
    return Response({"status":"success","data":res_data})
    

@api_view([GET])
def color(request):
    if request.method == GET:
        color_data = Color.objects.all()
        serializer = ColorSerializer(color_data,many= True)
        return Response(serializer.data)

# Create your views here.
@api_view([GET, POST, PUT, PATCH, DELETE])
@decorator_func
def user(request, us):

    # GET METHOD
    if request.method == GET:
        objs = Person.objects.all()
       
        # use of related_name field it binds the foreign key table to primary key 
        # color = Color.objects.get(color_name = 'Red')
        # print(color.fav_color.all())
        # if related_name not given
        # print(color.person_set.all())
       
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)
    
    # POST METHOD
    elif request.method == POST:
        data = request.data
        serializer = PeopleSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)
    
    # PUT METHOD
    elif request.method == PUT:
        data = request.data
        obj = Person.objects.get(id=data["id"])
        serializer = PeopleSerializer(obj, data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)
    
    # PATCH METHOD
    elif request.method == PATCH:
        data = request.data
        print(data)
        obj = Person.objects.get(id=data["id"])

        serializer = PeopleSerializer(obj, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)
    
    # DELETE METHOD
    else:
        data = request.data
        print("data", data)
        obj = get_object_or_404(Person, id=data["id"])
        obj.delete()
        return Response(f"{data["id"]} is deleted")


