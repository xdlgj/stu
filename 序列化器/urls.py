from django.urls import path, re_path
from . import views
urlpatterns = [
    re_path(r'books/$', views.BookInfoView.as_view()),
    re_path(r'books/(?P<pk>\d+)/$', views.BookInfoDetailView.as_view()),
]
