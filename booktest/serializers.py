"""
序列化器的作用
1、序列化
2、反序列化
定义序列化器
1、定义类继承自Serializer
2、和模型类的字段名字一样
3、和模型类的字段类型一样
4、和模型类的字段选项一样（参数，比如默认值等）
    read_only=True, 序列化时使用id， 反序列化时不需要
    label： 字段说明
"""
from rest_framework import serializers
from booktest.models import BookInfo


# 1、定义书籍序列化器
class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='id', read_only=True)
    btitle = serializers.CharField(max_length=20, label='名称')
    bpub_date = serializers.DateTimeField(label='发布日期')
    bread = serializers.IntegerField(default=0, label='阅读量')
    bcomment = serializers.IntegerField(default=0, label='评论量')
    is_delete = serializers.BooleanField(default=False, label='逻辑删除')

    # 1、关联英雄、主键, 一方中序列化多方需要添加many=True
    # {'id': 2, 'btitle': '平凡的世界', 'bpub_date': '1980-05-01T00:00:00Z', 'bread': 200, 'bcomment': 10, 'is_delete': False, 'heroinfo_set': [1]}
    # heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # 2、关联英雄、使用模型类， __str__方法返回值
    #{'id': 2, 'btitle': '平凡的世界', 'bpub_date': '1980-05-01T00:00:00Z', 'bread': 200, 'bcomment': 10, 'is_delete': False, 'heroinfo_set': ['孙少平']}

    heroinfo_set = serializers.StringRelatedField(read_only=True, many=True)


class HeroInfoSerializer(serializers.Serializer):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    id = serializers.IntegerField(label='Id', read_only=True)
    hname = serializers.CharField(label='名字', max_length=20),
    hgender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    hcomment = serializers.CharField(label='描述信息', max_length=200, required=False, allow_blank=True)

    # 1、关联书籍外建，主键, {'id': 1, 'hgender': 1, 'hcomment': 'dsas', 'hbook': 2}
    # hbook = serializers.PrimaryKeyRelatedField(read_only=True)
    hbook = serializers.PrimaryKeyRelatedField(queryset=BookInfo.objects.all())
    # 2、关联书籍，使用模型类， __str__方法返回值
    # hbook = serializers.StringRelatedField(read_only=True)
    # 3、关联书籍序列化器  OrderedDict([('id', 2), ('btitle', '平凡的世界'), ('bpub_date', '1980-05-01T00:00:00Z'), ('bread', 200), ('bcomment', 10), ('is_delete', False)])
    # hbook = BookInfoSerializer()