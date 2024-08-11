from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Person, Color
from .serializer import PeopleSerializer, ColorSerializer
from rest_framework import status

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.core.paginator import Paginator
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


### APIView Class
class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        print(request.user.email)
        objs = Person.objects.all()

        # pagination
        page = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", 1)
        paginator = Paginator(objs, page_size)
        if page and int(page) > paginator.count:
            return Response(
                {"status": "error", "message": "page size invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PeopleSerializer(paginator.page(page), many=True)
        return Response(serializer.data)

    def post(self, request):
        return Response("this is POST")

    def put(self, request):
        return Response("this is PUT")

    def delete(self, request):
        return Response("This is Delete")


#### viewsets
class PeopleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post"]  # to allows only perticular methods
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get("search")
        queryset = self.queryset
        if search:
            queryset = queryset.filter(person_name__endswith=search)
        serializer = PeopleSerializer(queryset, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["GET"])
    def send_mail_to_person(self, request):
        return Response(
            {
                "status": "success",
                "message": "mail sent successfully",
            }
        )

    @action(detail=True, methods=["GET"])
    def fetch_and_send_mail_to_person(self, request, pk):
        print(pk)  # add primary key(slug)
        user = get_object_or_404(Person, id=pk)
        serializer = PeopleSerializer(user)
        print(serializer.data)
        return Response(
            {
                "status": "success",
                "message": "mail sent successfully",
                "data": serializer.data,
            }
        )


class ColorViewSet(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()
