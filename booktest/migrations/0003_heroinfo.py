# Generated by Django 3.0.8 on 2021-01-18 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0002_auto_20210115_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hname', models.CharField(max_length=20, verbose_name='名称')),
                ('hgender', models.SmallIntegerField(choices=[(0, 'female'), (1, 'male')], default=0, verbose_name='性别')),
                ('hcomment', models.CharField(max_length=200, null=True, verbose_name='描述信息')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('hbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booktest.BookInfo', verbose_name='图书')),
            ],
            options={
                'verbose_name': '英雄',
                'verbose_name_plural': '英雄',
                'db_table': 'tb_heros',
            },
        ),
    ]
