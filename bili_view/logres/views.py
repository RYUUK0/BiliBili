from django.shortcuts import render, HttpResponse, redirect
import json
from logres import myforms, models
from geetest import GeetestLib

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

# Create your views here.

# 处理请求滑动验证码的函数
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

#首页
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


# 登录函数
def login(request):
    if request.method == "POST":
        # 初始化登录状态字典
        ret = {'status': False, 'mes': None}
        # 获取极验所需验证信息
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        # 判断验证码是否正确
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        # 如果验证码正确,获取用户数据
        if result:
            # print(request.POST.get('username'))
            # print(request.POST.get('userpass'))
            userinfo = myforms.Login(request.POST)
            # 通过校验
            if userinfo.is_valid():
                request.session['login_user_name'] = userinfo.cleaned_data['username']
                ret['status'] = True
                ret['mes'] = '/index/'

            else:
                ret['mes'] = userinfo.errors
                # print(ret)

        return HttpResponse(json.dumps(ret))
    elif request.method == 'GET':
        form_obj = myforms.Login()
        return render(request, 'login.html', {'forms_obj': form_obj})

# 注册函数
def register(request):
    if request.method == 'GET':
        if request.userinfo:
            return redirect('/index/')
        # 传入空的表单对象生成HTML标签
        form_obj = myforms.Register()
        return render(request, 'resgister.html', {'forms_obj': form_obj})

    else:
        # 创建一个form对象
        reg_obj = myforms.Register(request.POST)
        # print(reg_obj)
        # 初始化状态信息
        res = {'status': False, 'mes': None}
        # 如果通过form校验
        if reg_obj.is_valid():
            print('通过校验')
            avator_img = request.FILES.get('avator')
            # 在数据库创建信息
            models.UserInfo.objects.create(avator=avator_img, **reg_obj.cleaned_data)

            # 改变状态信息
            res['status'] = True
            res['mes'] = '/login/'
            return HttpResponse(json.dumps(res))
        # 未通过form验证
        else:
            print("未通过验证")
            res['mes'] = reg_obj.errors
            return HttpResponse(json.dumps(res))
# 注销函数
def logoff(request):
    if request.session.get('login_user_name'):
        del request.session['login_user_name']
    return redirect('/index/')

# 设置函数
def settings(request):
    if request.method == 'GET':
        return render(request, 'user_set.html')

    else:
        change_field = request.POST.get('change')
        data = request.POST.get('data')
        res = {'success': False, 'reason': None}
        if data and change_field:
            data= json.loads(data)
            # print(data)
            # if change_field == 'name':
            #     new_username = data.get('new_username')
            #     print(new_username)
            #     print('修改名字')
            # elif change_field == 'password':
            #     old_password = data.get('old_password')
            #     new_password = data.get('new_password')
            #     re_password = data.get('re_password')
            #     print(old_password, new_password, re_password)
            #     print('修改密码')
            # elif change_field == 'email':
            #     new_email = data.get('new_email')
            #     print(new_email)
            #     print('修改邮箱')
            set_data = myforms.Clean_Set(change_field, data)
            #返回FALSE
            if set_data.updata_data():
                res['reason'] = '修改成功'
                res['success'] = True
            else:
                res['reason'] = set_data.errors
        else:
            res['reason'] = '请输入正确数据'

        return HttpResponse(json.dumps(res))