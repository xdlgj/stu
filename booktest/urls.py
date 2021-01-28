from django.urls import path, re_path
from . import views
urlpatterns = [
    re_path(r'books/$', views.BookListView.as_view()),
    re_path(r'books/(?P<book_id>\d+)/', views.BookDetailView.as_view())
]
