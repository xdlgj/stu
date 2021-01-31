from django.urls import path, re_path
from . import views
urlpatterns = [
    path('books/', views.BookListView.as_view()),
    re_path(r'^books/(?P<book_id>\d+)/', views.BookDetailView.as_view()),
    path('generic_books/', views.BookListGenericView.as_view()),
    # re_path(r'generic_books/(?P<pk>\d+)/', views.BookDetailGenericView.as_view()),
    re_path(r'generic_books/(?P<book_id>\d+)/', views.BookDetailGenericView.as_view()),
]
