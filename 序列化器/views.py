from django.shortcuts import render
from django.views import View
from .models import BookInfo
from django import http
import json
from booktest.serializers import BookInfoSerializer
from rest_framework.exceptions import ValidationError
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
        ser = BookInfoSerializer(data=dict_data)
        try:
            ser.is_valid(raise_exception=True)
        except ValidationError as error:
            return http.JsonResponse({
                'code': 405,
                'msg': next(iter(error.detail.values()))[0].title()
            })
        # 3、数据入库
        # book = BookInfo.objects.create(**dict_data)
        book = ser.save()
        # 4、返回响应
        return http.JsonResponse(book, status=201)


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
        book = BookInfo.objects.get(pk=pk)
        origin_data = BookInfoSerializer(instance=book).data
        origin_data.update(**dict_data)
        serializer = BookInfoSerializer(instance=book, data=origin_data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return http.JsonResponse({
                'code': 405,
                'msg': next(iter(e.detail.values()))[0].title()
            })
        # 3、数据入库
        serializer.save()
        # 4、返回响应
        return http.JsonResponse(serializer.data)

    def delete(self, request, pk):
        # 1、获取书籍
        book = BookInfo.objects.get(pk=pk)
        # 2、删除书籍
        book.delete()
        # 3、返回响应
        return http.HttpResponse(status=204)