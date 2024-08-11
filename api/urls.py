from home.views import index, user, color, login
from home.views_class import PersonAPI, PeopleViewSet, ColorViewSet
from home.view_toke import AuthAPI, RegisterAPI
from django.urls import path, include


############ ViewSet ###########
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"person", PeopleViewSet, basename="person")
router.register(r"color", ColorViewSet, basename="color")

urlpatterns = router.urls
############ ViewSet ###########

urlpatterns = [
    path("", include(router.urls)),
    # path("index/", index),
    # path("login/", login),
    # path("user/", user),
    # path("color/", color),
    # path("class/user", PersonAPI.as_view()),
    # path("register/", RegisterAPI.as_view()),
    # path("auth/login/", AuthAPI.as_view()),
]
