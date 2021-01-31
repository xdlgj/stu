from .models import BookInfo
from booktest.serializers import BookInfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView


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
"""
二级视图GenericAPIView
特点：
    1、继承自APIView,为列表视图和详情视图添加了常用的行为和属性
    2、可以和一个或多个mixin类配合使用
"""


# 使用二级视图实现列表视图
class BookListGenericView(GenericAPIView):
    """
    公共属性：
        queryset = None
        serializer_class = None
        lookup_field = 'pk'
        lookup_url_kwarg = None
        filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    公共方法：
        get_queryset(self):
            This method should always be used rather than accessing `self.queryset`
            directly, as `self.queryset` gets evaluated only once, and those results
            are cached for all subsequent requests.
        get_object(self)
        get_serializer(self, *args, **kwargs)
        get_serializer_class(self)
        get_serializer_context(self)
        filter_queryset(self, queryset)
        paginator(self)
        paginate_queryset(self, queryset)
        get_paginated_response(self, data)
    """
    # 使用公共的属性
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request):
        # 1、查询所有的书籍
        # books = self.queryset.all() 一般不使用这种方法
        books = self.get_queryset()
        # 2、将对象列表转换为字典列表
        # serializer = self.serializer_class(instance=books, many=True)
        # serializer = self.get_serializer_class()(instance=books, many=True)
        serializer = self.get_serializer(instance=books, many=True)
        # 3、返回响应
        return Response(serializer.data)

    def post(self, request):
        # 1、获取参数
        data_dict = request.data
        # 2、创建序列化器
        ser = self.get_serializer(data=data_dict)
        # 3、校验、数据入库
        ser.is_valid(raise_exception=True)
        ser.save()
        # 4、返回响应
        return Response(ser.data, status=status.HTTP_201_CREATED)


# 使用二级视图实现详情视图
class BookDetailGenericView(GenericAPIView):
    """
    详情视图：id，  get、 put、 delete
    get_object:

    """
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    lookup_url_kwarg = 'book_id'

    def get(self, request, book_id):
        # 1、查询书籍
        # 根据id获取到单个对象, 默认情况下id只能使用pk作为参数的key
        # 可以通过lookup_url_kwarg属性修改lookup_url_kwarg = 'book_id'
        book = self.get_object()
        # 2、将对象列表转换为字典列表
        serializer = self.get_serializer(instance=book)
        # 3、返回响应
        return Response(serializer.data)

    def put(self, req, book_id):
        data_dict = req.data
        book = self.get_object()
        ser = self.get_serializer(instance=book, data=data_dict)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def delete(self, request, book_id):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

