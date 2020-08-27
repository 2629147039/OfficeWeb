from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from django.contrib import messages
# Create your views here.
from managent import models
from managent import html_helper
from django.db.models import Q
from .models import Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):
    """
    index页面
    :param request:
    :return:
    """
    if not request.session.get('is_login'):
        return render(request, 'login/login.html', locals())
    return render(request, 'assets/index.html', locals())


# class MessageList(ModelForm):
#     class Meta:
#         model = models.Message  #对应的Model中的类
#         fields = "__all__"      #字段，如果是__all__,就是表示列出所有的字段
#         exclude = None          #排除的字段
#         help_texts = None       #帮助提示信息


##  代码编号：001
# def curd_index(request,pn=1):
#     #获取前端收到的查询的值，默认值为空
#     query=request.GET.get('name')
#     #如果存在，则对title和publisher进行模糊查询
#     if query:
#         book_obj = Message.objects.all().filter(Q(title__contains=query)|Q(publisher__name__contains=query))
#     #否则取得所有的记录，并设置query的初始值为''
#     else:
#         query = ''
#         book_obj=Message.objects.all()
#     #将取得的记录传给Paginator，每页显示5条
#     paginator=Paginator(book_obj, 5)
#     #这里做异常判断，稍后再讲
#     try:
#         page=paginator.page(pn)
#     except EmptyPage:
#         page=paginator.page(1)
#     #将page和查询字段传给前端
#     context={
#         'page':page,
#         'query':query,
#     }
#     return render(request, 'assets/companyFlow_sel.html', context=context)

def listing(request, page=1):
    books = models.Message.objects.all().order_by('id')
    paginator = Paginator(books, 2)
    num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
    page = paginator.page(int(num_p))
    return render(request, 'assets/page_test.html', locals())

    # contact_list = models.Message.objects.all()
    # paginator = Paginator(contact_list, 25)  # 每页显示25条
    #
    # page = request.GET.get('page')
    # print(page)
    # try:
    #     contacts = paginator.page(page)
    # except PageNotAnInteger:
    #     # 如果请求的页数不是整数，返回第一页。
    #     contacts = paginator.page(1)
    # except EmptyPage:
    #     # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
    #     contacts = paginator.page(paginator.num_pages)
    # return render(request, 'assets/companyFlow_sel.html', {'contacts': contacts})



# @csrf_exempt
def companyFlow_sel(request, pn=1):
    """
    留言index页面
    :param request:
    :return:
    """

    if not request.session.get('is_login'):
        return render(request, 'login/login.html', locals())
        # 获取前端收到的查询的值，默认值为空
    query = request.GET.get('query')
    # 如果存在，则对title和publisher进行模糊查询
    if query:
        print(request.GET.get('query'))
        msg_obj = models.Message.objects.all().filter(Q(tellphone__icontains=query) | Q(mess__icontains=query)
                                                      | Q(name__icontains=query)).order_by('c_time')
    # 否则取得所有的记录，并设置query的初始值为''
    else:
        query = ''
        msg_obj = models.Message.objects.all().order_by('c_time')
    paginator = Paginator(msg_obj, 20)
    # num_p = request.GET.get('page', 1)  # 以page为键得到默认的页面1
    # page = paginator.page(int(num_p))
    try:
        page = paginator.page(pn)
    except EmptyPage:
        page = paginator.page(1)
    context = {
        'page': page,
        'query': query,
    }
    return render(request, 'assets/companyFlow_sel.html', context=context)


    # 自制html_helper分页栏
    # per_item = 10
    # if page:
    #     pass
    # else:
    #     page = int(page)
    # start = (page - 1) * per_item
    # end = page * per_item
    # count = 10  #初始定义count

    # if request.method == 'POST':
    #     serch_list = request.POST
    #     if serch_list["name"] and serch_list["phone"]:
    #         name = serch_list["name"]
    #     elif serch_list["name"]:
    #         name = serch_list["name"]
    #     elif serch_list["phone"]:
    #         phone = serch_list["phone"]
    #     else:
    #         pass

    # count = models.Message.objects.all().count()
    #
    # result = models.Message.objects.all()[start:end]
    # if count % per_item == 0:
    #     all_pages_count = count / per_item
    # elif count < per_item:
    #     all_pages_count = 1
    # else:
    #     all_pages_count = count / per_item + 1
    # url = "companyFlow_sel"
    # page = html_helper.Page(page, all_pages_count, url)
    # ret = {'data': result, 'count': count, 'page': page}
    # return render_to_response('assets/companyFlow_sel.html', ret)


def message_del(request, id):
    obj = models.Message.objects.filter(id=id).first()
    obj.delete()
    return redirect('/managent/companyFlow_sel/1')

@csrf_exempt
def message_add(request):

    if not request.session.get('is_login'):
        return render(request, 'login/login.html', locals())

    if request.method == 'POST':
        messagelist ={}
        name = request.POST['name']
        message = request.POST['message']
        phone = request.POST['phone']
        mass = models.Message.objects.create(name=name, tellphone=phone, mess=message)
        mass.save()
        return HttpResponse("已收到您的留言，我们回尽快给您回复")
