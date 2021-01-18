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
反序列化
    校验：
        1、字段类型校验
        2、字段选项校验,比如最大长度， require默认为True， 有默认值的话（default）或require=False时可以不用传, read_only=True时不会被反序列化
        3、单字段校验（方法）方法名规范： validate_字段名
        4、多字段校验（方法）
        5、自定义校验（方法）在字段中添加validators参数为一个自定义校验方法的列表
    校验顺序：
        validate_btitle    3
        check_bpub_date    5
        validate           4

"""
from rest_framework import serializers
from booktest.models import BookInfo


# 自定义校验方法
def check_bpub_date(value):
    print('check_bpub_date')
    if value.year <= 2018:
        raise serializers.ValidationError('书籍的年份需要大于18年')
    return value


# 1、定义书籍序列化器
class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='id', read_only=True)
    btitle = serializers.CharField(max_length=20, label='名称')
    bpub_date = serializers.DateField(label='发布日期', validators=[check_bpub_date])
    bread = serializers.IntegerField(default=0, label='阅读量')
    bcomment = serializers.IntegerField(default=0, label='评论量')
    is_delete = serializers.BooleanField(default=False, label='逻辑删除')

    # 单字段校验
    def validate_btitle(self, value):
        print('validate_btitle')
        if 'xxx' in value:
            # rest_framework.exceptions.ValidationError: {'btitle': [ErrorDetail(string='书籍名中不能包含xxx', code='invalid')]}
            raise serializers.ValidationError('书籍名中不能包含xxx')
        return value

    # 多字段校验
    def validate(self, attrs):
        """
        :param attrs: 就是外界传进来的data（book_dict）
        :return:
        """
        print('validate')
        bread = attrs['bread']
        bcomment = attrs['bcomment']
        if bcomment > bread:
            raise serializers.ValidationError('评论量不能大于阅读量')
        return attrs

    # 1、关联英雄、主键, 一方中序列化多方需要添加many=True
    # {'id': 2, 'btitle': '平凡的世界', 'bpub_date': '1980-05-01T00:00:00Z', 'bread': 200, 'bcomment': 10, 'is_delete': False, 'heroinfo_set': [1]}
    # heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # 2、关联英雄、使用模型类， __str__方法返回值
    #{'id': 2, 'btitle': '平凡的世界', 'bpub_date': '1980-05-01T00:00:00Z', 'bread': 200, 'bcomment': 10, 'is_delete': False, 'heroinfo_set': ['孙少平']}

    # heroinfo_set = serializers.StringRelatedField(read_only=True, many=True)


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