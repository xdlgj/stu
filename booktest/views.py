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
