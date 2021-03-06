# Generated by Django 2.1.7 on 2019-04-07 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25, null=True, unique=True)),
                ('phone', models.CharField(max_length=11, null=True, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, '已删除'), (1, '待激活'), (2, '正常')])),
                ('avator', models.FileField(default='avators_pic/111.png', upload_to='avators_pic/', verbose_name='头像')),
            ],
        ),
    ]
