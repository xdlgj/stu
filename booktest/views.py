from django.shortcuts import render
from django.views import View
from .models import BookInfo
from django import http
import json
from booktest.serializers import BookInfoSerializer
# Create your views here.


class BookInfoView(View):

    def get(self, request):
        # 1、查询所有的书籍
        books = BookInfo.objects.all()
        # 2、数据转换
        serializer = BookInfoSerializer(instance=books, many=True)
        # 3、返回响应
        return http.JsonResponse(serializer.data, safe=False)

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
        serializer = BookInfoSerializer(instance=book)
        return http.JsonResponse(serializer.data, status=201)


class BookInfoDetailView(View):

    def get(self, request, pk):
        # 1、通过pk获取对象
        book = BookInfo.objects.get(pk=pk)
        # 2、数据转换
        serializer = BookInfoSerializer(instance=book)
        # 3、返回响应
        return http.JsonResponse(serializer.data)

    def put(self, request, pk):
        # 1、获取参数
        dict_data = json.loads(request.body.decode())
        # 2、校验参数
        # 3、数据入库
        BookInfo.objects.filter(pk=pk).update(**dict_data)
        book = BookInfo.objects.get(pk=pk)
        serializer = BookInfoSerializer(instance=book)
        # 4、返回响应
        return http.JsonResponse(serializer.data)

    def delete(self, request, pk):
        # 1、获取书籍
        book = BookInfo.objects.get(pk=pk)
        # 2、删除书籍
        book.delete()
        # 3、返回响应
        return http.HttpResponse(status=204)