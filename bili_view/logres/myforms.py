from django import forms
from logres import models
from django.core.exceptions import ValidationError



#注册的表单类
class Register(forms.Form):
    username = forms.CharField(
        max_length = 16,
        min_length = 6,
        required = True,
        label = '账户',
        error_messages = {
            'max_length': '最大长度不能超过16',
            'min_length': '最小长度不能低于6',
            'required': '用户输入不能为空'
        },
        widget = forms.widgets.TextInput(
            attrs = {'class': 'form-control'},
        )
    )
    password = forms.CharField(
        max_length=16,
        min_length=6,
        required=True,
        label = '密码',
        error_messages={
            'max_length': '最大长度不能超过16',
            'min_length': '最小长度不能低于6',
            'required': '用户输入不能为空'
        },
        widget = forms.widgets.PasswordInput(
            attrs = {'class': 'form-control'},
            render_value = True,
        )
    )
    phone = forms.IntegerField(
        required=True,
        label = '电话',
        error_messages={
            'required': '用户输入不能为空'
        },
        widget = forms.widgets.TextInput(
            attrs = {'class': 'form-control'},
        )
    )

    #重写clean函数，对输入数据进行进一步校验
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        is_alive = models.UserInfo.objects.filter(phone = phone).first()
        #电话存在
        if is_alive:
            self.add_error('phone', ValidationError('电话已存在'))
        else:
            return self.cleaned_data['phone']

    def clean_username(self):
        input_user = self.cleaned_data.get('username')
        is_alive = models.UserInfo.objects.filter(username = input_user).first()
        # 返回结果为真--》存在相同用户名
        if is_alive:
            self.add_error('username', ValidationError('用户已存在'))
        else:
            return self.cleaned_data['username']


#登录的表单类
class Login(forms.Form):
    username = forms.CharField(
        max_length = 16,
        min_length = 6,
        required = True,
        label = '用户名',
        widget = forms.widgets.TextInput(
            attrs = {'class': 'form-control'},
        ),
        error_messages = {
            'max_length': '长度不能超过16',
            'min_length': '长度不能小于8',
            'required': '用户名不能为空',
        },
    )
    password = forms.CharField(
        max_length = 16,
        min_length = 6,
        required = True,
        label = '密码',
        widget = forms.widgets.PasswordInput(
            attrs = {'class': 'form-control'},
            render_value = True,
        ),
        error_messages={
            'max_length': '长度不能超过16',
            'min_length': '长度不能小于8',
            'required': '请输入密码',
        },
    )

    #username的检验函数
    def clean_username(self):
        get_name = self.cleaned_data.get('username')
        #从数据库中检验用户是否存在
        is_alive = models.UserInfo.objects.filter(username = get_name).first()
        #如果不存在
        if not is_alive:
            self.add_error('username', ValidationError('用户不存在'))
        else:
            return self.cleaned_data['username']

    def clean(self):
        get_name = self.cleaned_data.get('username')
        get_pass = self.cleaned_data.get('password')
        user_obj = models.UserInfo.objects.filter(username = get_name).first()
        #print(type(get_name))
        #print('账户名是',get_name)
        #print(type(get_pass))
        #print('获得的密码是', get_pass)

        #密码验证
        if user_obj and get_pass == user_obj.password:
            #print(user_obj.password)
            return self.cleaned_data
        else:
            self.add_error('password', ValidationError('密码错误'))


class Set_Username(forms.Form):
    user_id = forms.IntegerField(required = True)
    new_username = forms.CharField(required = True,
                               max_length = 20,
                               min_length = 5,
                               error_messages = {
                                   'required': '请输入新用户名',
                                   'min_length': '最小长度为5',
                                   'max_length': '最大长度为20',
                               })

class Set_Password(forms.Form):
    user_id = forms.IntegerField(required=True)
    old_password = forms.IntegerField(required = True,
                                      error_messages = {
                                          'required': '请输入旧密码',
                                      })
    new_password = forms.IntegerField(required = True,
                                      error_messages = {
                                          'required': '请输入旧密码',
                                      })
    re_password = forms.IntegerField(required = True,
                                      error_messages = {
                                          'required': '请输入旧密码',
                                      })

    def clean_old_password(self):
        print('data is >>>>>>>>>>>>>>>>>>', self.data)
        user_pk = self.data.get('user_id')
        user_password = models.UserInfo.objects.filter(pk = user_pk).values('password').first()['password']
        if self.data.get('old_password') != user_password:
            self.add_error('old_password', ValidationError('原密码错误'))
        else:
            return self.cleaned_data['old_password']

    def clean(self):
        re_password = self.cleaned_data['re_password']
        new_password = self.cleanec_data['new_password']
        if re_password and re_password != new_password:
            self.add_error('re_password', ValidationError('两次密码不一致'))
        else:
            return self.cleaned_data

class Set_Phone(forms.Form):
    user_id = forms.IntegerField(required=True)
    new_phone = forms.IntegerField(required = True,
                               error_messages = {
                                   'required': '请输入新phone',
                               })



#设置数据校验
class Clean_Set():

    def __init__(self, change, data):
        self.change = change
        self.data = data
        self.user_id = self.data.get('user_id')
        self.user_obj = None or models.UserInfo.objects.filter(pk = self.user_id)
        self.errors = None


    def updata_data(self):
        if self.change == 'name':
            check = Set_Username(self.data)
            if check.is_valid() and self.user_obj:
                self.user_obj.update(username = check.cleaned_data['new_username'])
                return True
            else:
                self.errors = check.errors

        elif self.change == 'password':
            check = Set_Password(self.data)
            if check.is_valid() and self.user_obj:
                self.user_obj.update(password = check.cleaned_data['new_password'])
                return True
            else:
                self.errors = check.errors

        elif self.change == 'phone':
            check = Set_Phone(self.data)
            if check.is_valid() and self.user_obj:
                self.user_obj.update(phone = check.cleaned_data['new_phone'])
                return True
            else:
                self.errors = check.errors

        else:
            self.errors = '发生未知错误'
            return False