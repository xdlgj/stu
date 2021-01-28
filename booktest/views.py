from .models import BookInfo
from booktest.serializers import BookInfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# 1、定义类，继承APIView(一级视图), 列表视图：get post
class BookListView(APIView):
    """
    View获取数据的方式：
        1、GET
            request.GET
        2、POST
            request.POST： 取表单数据
            request.body： 取json数据
    APIView获取数据的方式：
        1、GET
            request.query_params
        2、POST
            request.data
    Response: 可以取代Django中自带HttpResponse、JsonResponse...
    """
    def get(self, request):
        # 1、查询所有的书籍
        books = BookInfo.objects.all()
        # 2、将对象列表转换为字典列表
        serializer = BookInfoSerializer(instance=books, many=True)
        # 3、返回响应
        return Response(serializer.data)

    def post(self, request):
        # 1、获取参数
        data_dict = request.data
        # 2、创建序列化器
        ser = BookInfoSerializer(data=data_dict)
        # 3、校验、数据入库
        ser.is_valid(raise_exception=True)
        ser.save()
        # 4、返回响应
        return Response(ser.data, status=status.HTTP_201_CREATED)


class BookDetailView(APIView):
    """
    详情视图：id，  get、 put、 delete
    """
    def get(self, request, book_id):
        # 1、查询书籍
        book = BookInfo.objects.get(id=book_id)
        # 2、将对象列表转换为字典列表
        serializer = BookInfoSerializer(instance=book)
        # 3、返回响应
        return Response(serializer.data)

    def put(self, req, book_id):
        data_dict = req.data
        book = BookInfo.objects.get(id=book_id)
        ser = BookInfoSerializer(instance=book, data=data_dict)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def delete(self, request, book_id):
        BookInfo.objects.get(id=book_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
