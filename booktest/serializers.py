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


# 1、定义书籍序列化器
class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='id', read_only=True)
    btitle = serializers.CharField(max_length=20, label='名称')
    bpub_date = serializers.DateTimeField(label='发布日期')
    bread = serializers.IntegerField(default=0, label='阅读量')
    bcomment = serializers.IntegerField(default=0, label='评论量')
    is_delete = serializers.BooleanField(default=False, label='逻辑删除')