from django.urls import path, re_path
from . import views
urlpatterns = [
    path('books/', views.BookListView.as_view()),
    re_path(r'^books/(?P<book_id>\d+)/', views.BookDetailView.as_view()),
    path('generic_books/', views.BookListGenericView.as_view()),
    # re_path(r'generic_books/(?P<pk>\d+)/', views.BookDetailGenericView.as_view()),
    re_path(r'generic_books/(?P<book_id>\d+)/', views.BookDetailGenericView.as_view()),
    path('mixin_books/', views.BookListMixinView.as_view()),
    re_path(r'mixin_books/(?P<book_id>\d+)/', views.BookDetailMixinView.as_view()),
    path('third_books/', views.BookListThirdView.as_view()),
    re_path(r'third_books/(?P<book_id>\d+)/', views.BookDetailThirdView.as_view()),
    path('viewset_books/', views.BookViewSet.as_view({'get': 'list'})),
    re_path(r'^viewset_books/(?P<book_id>\d+)/', views.BookViewSet.as_view({'get': 'retrieve'})),
    path('genericviewset_books/', views.BookGenericViewSet.as_view({'get': 'list'})),
    re_path(r'genericviewset_books/(?P<book_id>\d+)/', views.BookGenericViewSet.as_view({'get': 'retrieve'})),
    path('ro_books/', views.BookROViewSet.as_view({'get': 'list'})),
    re_path(r'ro_books/(?P<pk>\d+)/', views.BookROViewSet.as_view({'get': 'retrieve'})),
    path('modelviewset_books/', views.BookModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'modelviewset_books/(?P<pk>\d+)/', views.BookModelViewSet.as_view({'get': 'retrieve',
                                                                               'put': 'update', 'delete': 'destroy'})),
    path('bread_books/', views.BookInfoModelViewSet.as_view({'get': 'bread_gt20'})),
    re_path('bread_books/(?P<pk>\d+)/', views.BookInfoModelViewSet.as_view({'put': 'update_bread'}))
]
