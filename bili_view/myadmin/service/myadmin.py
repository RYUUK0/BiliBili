from django.urls import path, re_path
from django.shortcuts import render, HttpResponse, redirect
from myadmin import templates
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from myadmin.tags import MyPage
from django.db.models import Q
from django.db.models.fields.related import ManyToManyField, ForeignKey
import copy
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.core.handlers.wsgi import WSGIRequest

#获得数据表单的类
class ShowList:
    def __init__(self,model_myadmin, html_request, data_obj):
        """
        :param model_myadmin: 传入的数据表配置类
        :param html_request: html请求
        :param data_list: 需要展示的数据
        """
        self.model_myadmin = model_myadmin
        self.data = data_obj
        self.request = html_request
        self.base_url = html_request.path
        #self.page_obj = MyPage(self.request.GET.get('page'), 10, self.get_body(), self.request.GET)
        self.actions = model_myadmin.actions
        self.filters = model_myadmin.filter_list

    #表头数据
    def get_head(self):
        head_data = []
        for detail in self.model_myadmin.display:
            if isinstance(detail, str):
                if detail == "__str__":
                    field_name = self.model_myadmin.model_name.upper()
                else:
                    #得到相应的字段对象,获得verbose_name
                    field_obj = self.model_myadmin.model._meta.get_field(detail)
                    field_name = field_obj.verbose_name
                    if detail in self.model_myadmin.sort_list:
                        field_name = mark_safe("<a href='?sort_field=%s'>%s</a>"%(detail, field_name))

            else:
                field_name = detail(self.model_myadmin, obj = None, is_head = True)
            head_data.append(field_name)

        return head_data
    #表单body数据
    def get_body(self):
        body_data = []
        for each in self.data.content:
            #循环字段列表,创建个人信息的列表
            each_info = []
            for field in self.model_myadmin.display:
                if isinstance(field, str):
                    if field == '__str__':
                        res = each.__str__()
                    else:
                        field_obj = self.model_myadmin.model._meta.get_field(field)
                        if isinstance(field_obj, ManyToManyField):
                            r = []
                            for i in getattr(each, field).all()[: 8]:
                                r.append(str(i))
                            res = ",".join(r)

                        else:
                            #利用反射得到该属性的值
                            res = getattr(each, field)
                            if field in self.model_myadmin.display_links:
                                res_url = reverse(self.model_myadmin.change_url_name, args = (each.id, ))
                                res = mark_safe('<a href="%s">%s</a>'%(res_url, res))
                else:
                    res = field(self.model_myadmin, each)
                #添加到个人信息列表
                each_info.append(res)
            #将个人信息添加到总列表中
            body_data.append(each_info)
        return body_data

    def get_actions(self):
        res = []
        for each in self.actions:
            func_dict = {}
            func_dict["name"] = each.__name__

            func_dict["desc"] = each.desc or each.__name__
            res.append(func_dict)
        return res

    def get_filter(self):
        all_filter_dict = {}
        for field in self.filters:
            parms = copy.deepcopy(self.request.GET)
            filter_list = []
            field_obj = self.model_myadmin.model._meta.get_field(field)
            #生成本字段的 "全部" 筛选条件的URL
            if self.request.GET.get(field):
                del parms[field]

            _url = parms.urlencode()
            the_all = mark_safe("<a href='?%s'>全部</a>"%_url)
            filter_list.append(the_all)
            if isinstance(field_obj, ManyToManyField) or isinstance(field_obj, ForeignKey):
                for row in field_obj.related_model.objects.all()[: 5]:
                    parms[field] = row.pk
                    _url = parms.urlencode()
                    res = mark_safe('<a href="?%s">%s</a>'%(_url, str(row)))
                    filter_list.append(res)

            #field_boj为普通字段
            else:
                for row in self.model_myadmin.model.objects.all()[self.data.start: self.data.end]:
                    name = getattr(row, field)
                    parms[field] = name
                    _url = parms.urlencode()
                    res = mark_safe('<a href="?%s">%s</a>'%(_url, name))
                    filter_list.append(res)
            all_filter_dict[field] = filter_list

        return all_filter_dict

    def get_modeldict(self):
        model_dict = {}
        #print(type(self.model_myadmin.site._registry))
        for model, model_admin in self.model_myadmin.site._registry.items():
            model_name = model_admin.model_name
            model_url = reverse(model_admin.look_url_name)
            model_dict[model_name] = model_url

        return model_dict


#单个模型表的配置类
class ModelMyadmin(object):
    #默认返回HTML标签的函数
    def edit_tag(self, obj, is_head = False):
        if not is_head:
            res = "<a href='%s'>编辑</a>"%reverse(self.change_url_name, args = (obj.pk, ))
        else:
            res = "操作"
        return mark_safe(res)
    #返回选择框
    def select(self, obj, is_head = False):
        if not is_head:
            res = "<input type='checkbox' value='%s' class='select_item' name='select_pk' />" % obj.pk
        else:
            res = "<input type='checkbox' id='queryset_select'/>"

        return mark_safe(res)
    #批量操作
    def act_update(self, queryset):
        pass
    act_update.desc = act_update.__name__
    #默认显示字段列表
    display = [
        select, "__str__", edit_tag]
    #字段名有连接的字段
    display_links = ["name", ]
    #默认可被所搜的字段
    search_fields = []
    #操作列表
    actions = []
    #用于筛选的字段列表
    filter_list = []
    #默认用于排序的字段
    sort_list = []

    def __init__(self, model, site):
        self.model = model
        self.site = site

        #传入模型表的名称和APP名称
        self.model_name = model._meta.model_name
        self.app_name = model._meta.app_label

        #四个URL名称
        self.look_url_name = "%s_%s_look"%(self.app_name, self.model_name)
        self.delete_url_name = "%s_%s_delete"%(self.app_name, self.model_name)
        self.change_url_name = "%s_%s_change"%(self.app_name, self.model_name)
        self.add_url_name = "%s_%s_add"%(self.app_name, self.model_name)


    #得到配置表单
    def get_modelform(self):
        class SelfModelForm(ModelForm):
            class Meta:
                model = self.model
                fields = "__all__"

        return SelfModelForm

    #查询方法
    def search(self):
        search_obj = Q()
        if self.search_key:
            search_obj.connector = "or"
            for search_field in self.search_fields:
                search_obj.children.append((search_field + "__contains", self.search_key))

            search_data = self.model.objects.filter(search_obj)
        else:
            search_data = self.model.objects.all()
        return search_data


    #筛选
    def filter(self, request, data):
        filter_dict = request.GET
        if filter_dict:
            filter_obj = Q()
            filter_obj.connector = "and"
            for filter_name, filter_val in filter_dict.items():
                if filter_name in self.filter_list:
                    #print('筛选条件>>>>', filter_name, filter_val)
                    #print('类型》》》》》》', type(filter_name), type(filter_val))
                    filter_obj.children.append((filter_name, filter_val))
            data = data.filter(filter_obj)

        return data

    def field_sort(self, data):
        clean_data = data.all().order_by('-' + self.sort_field)
        return clean_data

    #对应的增删改查视图函数
    def look(self, request):
        #首先得到查询条件,在查询结果
        search_key = request.GET.get('search_key', "")
        self.search_key = search_key
        #执行搜索
        clean_data = self.search()

        #执行筛选
        clean_data = self.filter(request, clean_data)

        #执行排序
        sort_field = request.GET.get('sort_field', "")
        self.sort_field = sort_field
        if self.sort_field:
            print(self.sort_field)
            clean_data = self.field_sort(clean_data)




        #批量操作用POST传数据
        if request.method == "POST":
            pk_list = request.POST.getlist('select_pk')
            action_name = request.POST.get('actions_name')
            if action_name and pk_list:
                print(action_name, type(action_name))
                queryset_list = self.model.objects.filter(pk__in = pk_list)
                func = getattr(self, action_name)
                func(queryset_list)
        length = len(clean_data)
        print('type is ............', type(clean_data))
        data_obj = MyPage(request.GET.get('page'), 10, clean_data, length, get_dict = request.GET)

        print(type(data_obj.content))
        #定制一个展示页面类
        showlist = ShowList(self, request, data_obj = data_obj)
        add_url = reverse(self.add_url_name)

        return render(request, 'myadmin_look.html', locals())

    def add(self, request):
        #print('访问数据对象:', self.model)
        modelform = self.get_modelform()
        forms = modelform()
        for each in forms:
            if isinstance(each.field, ModelChoiceField):
                #each.field.queryset.model获得字段的关联表对象
                link_app = each.field.queryset.model._meta.app_label
                link_model = each.field.queryset.model._meta.model_name
                each.is_pop = True
                each.url = reverse("%s_%s_add"%(link_app, link_model))

        if request.method == 'POST':
            forms = modelform(request.POST)
            if forms.is_valid():
                print(forms.cleaned_data)
                forms.save()
                return redirect(reverse(self.look_url_name))
        return render(request, "myadmin_add.html", locals())

    def delete(self, request, delete_id):
        #print('访问数据对象:', self.model)
        return HttpResponse('删除')

    def change(self, request, change_id):
        #print('访问数据对象:', self.model)
        modelform = self.get_modelform()
        change_obj = self.model.objects.filter(pk = change_id).first()
        forms = modelform(instance = change_obj)
        if request.method == 'POST':
            forms = modelform(request.POST, instance = change_obj)
            if forms.is_valid():
                forms.save()
                return redirect(reverse(self.look_url_name))
        return render(request, 'myadmin_change.html', locals())


    # 二级URL分发(增删改查)
    def get_urls_two(self):
        res = []
        res.append(re_path(r'^$', self.look, name = self.look_url_name))
        res.append(re_path(r'^add/$', self.add,  name = self.add_url_name))
        res.append(re_path(r'^(\d+)/delete/$', self.delete,  name = self.delete_url_name))
        res.append(re_path(r'^(\d+)/change/$', self.change,  name = self.change_url_name))
        return res

    @property
    def url_two(self):
        return (self.get_urls_two(), None, None)

#关于模型注册， URL一级分发
class MyadminSite(object):
    def __init__(self):
        self._registry = {}

    def register(self, model, admin_class = ModelMyadmin, **options):

        self.admin_class = admin_class
        self._registry[model] = self.admin_class(model, self)

    #一级URL分发
    def get_urls(self):
        res = []
        for model, model_admin in self._registry.items():
            model_name = model._meta.model_name
            app_name = model._meta.app_label
            target = re_path(r'^{0}/{1}/'.format(app_name, model_name), model_admin.url_two)
            res.append(target)
        return res

    @property
    def urls(self):
        return (self.get_urls(), None, None)

    def index(self, request):
        url_dict = {}
        print(self._registry)
        for model, model_admin in self._registry.items():
            model_name = model._meta.model_name
            app_name = model._meta.app_label
            url_dict[model_name] = r'myadmin/{0}/{1}/'.format(app_name, model_name)
        print(url_dict)
        return render(request, 'myadmin_look.html', {'url_dict': url_dict})

site = MyadminSite()