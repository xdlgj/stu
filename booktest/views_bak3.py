"""
1、序列化器，序列化单个书籍对象
"""
from booktest.serializers import BookInfoSerializer
from booktest.models import BookInfo


# 1、获取书籍对象
book = BookInfo.objects.get(pk=2)
# 2、创建序列化器, instance表示序列化的对象
serializer = BookInfoSerializer(instance=book)
# 3、转换数据
print(serializer.data)
"""
2、序列化列表对象
"""
from booktest.serializers import BookInfoSerializer
from booktest.models import BookInfo
# 1、获取书籍对象列表
books = BookInfo.objects.all()
# 2、创建序列化器, instance表示序列化的对象
serializer = BookInfoSerializer(instance=books, many=True)
# 3、转换数据
print(serializer.data)
"""
结果：
[
OrderedDict([('id', 2), ('btitle', '平凡的世界'), ('bpub_date', '1980-05-01T00:00:00Z'), ('bread', 200), ('bcomment', 10), ('is_delete', False)]), 
OrderedDict([('id', 3), ('btitle', '平凡的世界'), ('bpub_date', '1980-05-01T00:00:00Z'), ('bread', 20), ('bcomment', 10),'is_delete', False)]), 
OrderedDict([('id', 4), ('btitle', '白鹿原'), ('bpub_date', '2021-01-17T22:24:00Z'), ('bread', 0), ('bcomment', 0), ('is_delete', False)])
]
"""
"""
3、序列英雄
"""
from booktest.serializers import HeroInfoSerializer
from booktest.models import HeroInfo
# 1、获取英雄对象
hero = HeroInfo.objects.get(id=1)
# 2、创建序列化器, instance表示序列化的对象
serializer = HeroInfoSerializer(instance=hero)
# 3、转换数据
print(serializer.data)
"""
4、反序列化，书籍对象
"""
from booktest.serializers import BookInfoSerializer
# 1、准备数据
book_dict = {
    "btitle": "活着",
    "bpub_date": "2020-1-01",
    "bread": "50",
    "bcomment": "20",
}
# 2、创建序列化器
serializer = BookInfoSerializer(data=book_dict)
# serializer.is_valid()
serializer.is_valid(raise_exception=True)
# 3、输出
print(serializer.data)
"""
5、反序列化创建对象入库
"""
from booktest.serializers import BookInfoSerializer
# 1、准备数据
book_dict = {
    "btitle": "活着",
    "bpub_date": "2020-1-01",
    "bread": "50",
    "bcomment": "20",
}
# 2、创建序列化器
serializer = BookInfoSerializer(data=book_dict)
serializer.is_valid(raise_exception=True)
# 3、入库，会调用序列化器中的create方法
serializer.save()
"""
6、反序列化更新对象
"""
from booktest.serializers import BookInfoSerializer
from booktest.models import BookInfo
# 1、准备数据
book_dict = {
    "bread": "5",
}
# 2、创建序列化器
book = BookInfo.objects.get(pk=6)
origin_data = BookInfoSerializer(instance=book).data
origin_data.update(**book_dict)
serializer = BookInfoSerializer(instance=book, data=origin_data, partial=True)
serializer.is_valid(raise_exception=True)
# 3、入库，会调用序列化器中的update方法
serializer.save()

'''*****************使用ModelSerializer,进行序列化**********************'''
from booktest.serializers import BookInfoModelSerializer
from booktest.models import BookInfo
book = BookInfo.objects.get(pk=7)
serializer = BookInfoModelSerializer(instance=book)
serializer.data  # {'id': 7, 'btitle': '活着', 'bpub_date': '2019-05-01', 'bread': 30, 'bcomment': 10, 'is_delete': False}

'''*****************使用ModelSerializer,进行反序列化**********************'''
from booktest.serializers import BookInfoModelSerializer
book_dict = {
    "btitle": "平凡的世界",
    "bpub_date": "2020-1-01",
    "bread": "50",
    "bcomment": "20",
}
serializer = BookInfoModelSerializer(data=book_dict)
serializer.is_valid(raise_exception=True)
serializer.save()
"""
调用save()方法出现下面报错的原因是： 在调用save()方法之前调用了serializer.data
AssertionError: You cannot call `.save()` after accessing `serializer.data`.
If you need to access data before committing to the database then inspect 'serializer.validated_data' instead.
"""