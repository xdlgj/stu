from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import BookInfo


# 1、定义序列化器
class BookInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = '__all__'


# 2、视图集
class BookInfoModelViewSet(ModelViewSet):
    serializer_class = BookInfoModelSerializer
    queryset = BookInfo.objects.all()