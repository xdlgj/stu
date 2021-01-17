from django.urls import path, re_path
from . import views
from rest_framework.routers import DefaultRouter
urlpatterns = [
]
# drf中的路由
router = DefaultRouter()
router.register(r'books', views.BookInfoModelViewSet, basename='books')
urlpatterns += router.urls
