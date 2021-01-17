from django.shortcuts import render
from django.views import View
from .models import BookInfo
from django import http
import json
# Create your views here.


class BookInfoView(View):

    def get(self, request):
        # 1、查询所有的书籍
        books = BookInfo.objects.all()
        # 2、数据转换

        book_list = []
        for book in books:
            book_dict = {
                'id': book.id,
                'btitle': book.btitle,
                'bpub_date': book.bpub_date,
                'bread': book.bread,
                'bcomment': book.bcomment,
            }
            book_list.append(book_dict)
        # 3、返回响应
        return http.JsonResponse(book_list, safe=False)

    def post(self, request):
        # 1、获取参数
        dict_data = json.loads(request.body.decode())
        btitle = dict_data.get('btitle')
        bpub_date = dict_data.get('bpub_date')
        bread = dict_data.get('bread')
        bcomment = dict_data.get('bcomment')
        # 2、校验参数

        # 3、数据入库
        book = BookInfo.objects.create(**dict_data)
        # 4、返回响应
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
        }
        return http.JsonResponse(book_dict, status=201)


class BookInfoDetailView(View):

    def get(self, request, pk):
        # 1、通过pk获取对象
        book = BookInfo.objects.get(pk=pk)
        # 2、数据转换
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
        }
        # 3、返回响应
        return http.JsonResponse(book_dict)

    def put(self, request, pk):
        # 1、获取参数
        dict_data = json.loads(request.body.decode())
        # 2、校验参数
        # 3、数据入库
        BookInfo.objects.filter(pk=pk).update(**dict_data)
        book = BookInfo.objects.get(pk=pk)
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
        }
        # 4、返回响应
        return http.JsonResponse(book_dict)

    def delete(self, request, pk):
        # 1、获取书籍
        book = BookInfo.objects.get(pk=pk)
        # 2、删除书籍
        book.delete()
        # 3、返回响应
        return http.HttpResponse(status=204)