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
