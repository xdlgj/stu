from .models import BookInfo
from django.shortcuts import get_object_or_404
from booktest.serializers import BookInfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, \
    DestroyAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet, ReadOnlyModelViewSet


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


"""
Mixin特点:
    1、mixin类提供用于提供基本视图行为（列表视图、详情视图）的操作
    2、配合二级视图GenericAPIView使用
类名                提供方法                功能
ListModelMixin      list                  查询所有数据
CreateModelMixin    create                创建单个对象

RetrieveModelMixin  retrieve              获取单个对象
UpdateModelMixin    update                更新单个对象
DestroyModelMixin   destroy               删除单个对象           
"""


class BookListMixinView(GenericAPIView, ListModelMixin, CreateModelMixin):
    # 使用公共的属性
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BookDetailMixinView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    """
    详情视图：id，  get、 put、 delete
    get_object:

    """
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    lookup_url_kwarg = 'book_id'

    def get(self, request, book_id):
        return self.retrieve(request)

    def put(self, req, book_id):
        return self.update(req)

    def delete(self, request, book_id):
        return self.destroy(request)
"""
三级视图：如果没有大量自定义行为（比如发送短信，上传图片），可以使用通用视图解决
类名                      父类（都继承GenericAPIView）          提供方法                  功能
CreateAPIView            CreateModelMixin                    post                    创建单个对象
ListAPIView              ListModelMixin                      get                     查询所有数据
RetrieveAPIView          RetrieveModelMixin                  get                     获取单个对象
UpdateAPIView            UpdateModelMixin                    put                     更新单个对象
DestroyAPIView           DestroyModelMixin                   delete                  删除单个对象
"""


class BookListThirdView(ListCreateAPIView):
    # 使用公共的属性
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer


class BookDetailThirdView(RetrieveUpdateDestroyAPIView):
    """
    详情视图：id，  get、 put、 delete
    get_object:

    """
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    lookup_url_kwarg = 'book_id'
"""
视图集特点：
    1、可以将一组相关的操作放在一个类中进行完成
    2、不提供get、post方法，使用retrieve、create方法来替代
    3、可以将标准的请求方式（get、post、put、delete）和mixin中的方法做映射
常见的视图集
类名                      父类                                作用                     
ViewSet                  APIView,                           可以做路由映射 
                         ViewSetMixin(重写as_view)           可以提供路由映射，可以使用三个属性，三个方法
GenericViewSet           GenericAPIView
                         ViewSetMixin(重写as_view)
ModelViewSet             GenericViewSet,                    所有的增删改查功能，可以使用三个属性，三个方法
                         5个mixin类
ReadOnlyModelViewSet     GenericViewSet，                    获取单个和多个，可以使用三个属性，三个方法
                         ListModelMixin，
                         RetrieveModelMixin
"""


class BookViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = BookInfo.objects.all()
        serializer = BookInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, book_id=None):
        queryset = BookInfo.objects.all()
        book = get_object_or_404(queryset, pk=book_id)
        serializer = BookInfoSerializer(book)
        return Response(serializer.data)


class BookGenericViewSet(GenericViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, book_id=None):
        book = self.get_object()
        serializer = BookInfoSerializer(book)
        return Response(serializer.data)


class BookROViewSet(ReadOnlyModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer


class BookModelViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

