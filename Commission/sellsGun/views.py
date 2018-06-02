from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegForm
from .models import *
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from .matplotlibTools.pltUtils import *
import datetime
from django.http.response import JsonResponse
import json

####
#改写login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
)
from django.views.generic.edit import FormView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
####
products = ['lock','barrel','stock']
prices = {'lock':45,'stock':30,'barrel':25}

class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}
class LoginView(SuccessURLAllowedHostsMixin, FormView):
    """
    Display the login form and handle the login action.
    """
    form_class = AuthenticationForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/login.html'
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:

            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = "/"
        try:
            userType = User.objects.get(username=self.request.POST.get("username")).userType
            if userType=="boss":
                redirect_to="/pageadmin/"
            elif userType=="salesman":
                redirect_to = "/addOrder/"
        except ObjectDoesNotExist:
            redirect_to = "/users/login?next=/"
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context

def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
    redirecPath = request.POST.get("next",request.GET.get("next",''))
    return redirect(redirecPath)


def do_register(request):
    try:
        redirectPath = request.POST.get('next',request.GET.get('next','/'))
        if request.method=="POST":
            reg_form = RegForm(request.POST)

            if reg_form.is_valid():
                userType = request.POST.get('userType')
                username = request.POST.get('username')
                if userType == "boss":
                    redirect_to = "/pageadmin/"
                elif userType == "salesman":
                    redirect_to = "/addOrder/"
                reg_form.save()
                user = User.objects.get(username=username)
                auth_login(request, user)
                return redirect(redirect_to)
                
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
            return render(request,'reg.html',context={'form': reg_form,"next":redirectPath})
    except Exception as e:
        print(e)
        return render(request, 'failure.html', {'reason': reg_form.errors})

@login_required(login_url='/users/login?next=addOrder/')
def addOrder(request):
    username = request.user.username
    user = User.objects.get(username=username)
    now_time = datetime.datetime.now()
    try:
        comistionCheck = Commission.objects.get(salesId=user, commiDate__year=now_time.year, commiDate__month=now_time.month)
        clearingFlag = True
    except ObjectDoesNotExist:
        clearingFlag = False

    try:
        if request.method=="POST" and clearingFlag == False:
            stocksNumber = int(request.POST.get("stocks",0))
            locksNumber = int(request.POST.get("locks",0))
            barrelNumber = int(request.POST.get("barrels",0))
            city = request.POST.get('city')
            order = Order.objects.create(salesId=user,city=city)
            order.save()
            if stocksNumber>0:
                stocksOrder = OrderDetail.objects.create(orderId=order,product='stock',number=stocksNumber,total = stocksNumber * 30)
                stocksOrder.save()
            if locksNumber>0:
                lockOrder = OrderDetail.objects.create(orderId=order,product='lock',number=locksNumber,total = locksNumber * 45)
                lockOrder.save()
            if barrelNumber > 0 :
                barrelOrder = OrderDetail.objects.create(orderId = order,product='barrel',number=barrelNumber,total = barrelNumber * 25)
                barrelOrder.save()

        totalOrder=OrderDetail.objects.filter(orderId__salesId=user,orderId__date__month=now_time.month).values('product').annotate(count=Sum('number'))
        totalCount = {eachDict['product']:eachDict['count'] for eachDict in totalOrder}
        for key in products:
            if key  not in totalCount:
                totalCount[key]=0
        commission=calCommission(totalCount)
        nowCommission = {"commistion":commission[0],'percent':commission[1],"totalSale":commission[2]}
        orderTable = getOrderTable(user)
        remainCount ={'lock':70-totalCount['lock'],'stock':80-totalCount['stock'],'barrel':90-totalCount['barrel']}
        return render(request,"adminTemplates/userPage.html",{'orderTable':orderTable,\
                                              'totalCount':totalCount,\
                                              'remainCount':remainCount,\
                                              'nowCommission':nowCommission,\
                                              'clearingFlag':clearingFlag,\
                                                "username":username,\
                                                "aliasname":user.aliasName})
    except Exception as e:
        print(e)
        return render(request, 'failure.html', {'reason': str(e)})

@login_required(login_url='/users/login?next=addClearOrder/')
def clearingCommission(request):
    username = request.user.username
    user = User.objects.get(username=username)
    now_time = datetime.datetime.now()
    totalOrder = OrderDetail.objects.filter(orderId__salesId=user, orderId__date__month=now_time.month).values(
            'product').annotate(count=Sum('number'))
    totalCount = {eachDict['product']: eachDict['count'] for eachDict in totalOrder}
    for key in products:
        if key not in totalCount:
            totalCount[key] = 0
    try:
        comistion = Commission.objects.get(salesId=user,commiDate__year=now_time.year,commiDate__month=now_time.month)
        return render(request,"salesPersonClear.html",{
            "date": comistion.commiDate,
            "newClearing": False,
            "totalSale":comistion.sellCount,
            "commistion":comistion.commission,
            "totalCount": totalCount
        })
    except ObjectDoesNotExist:
        commissionCount = calCommission(totalCount)
        salesGunFalg = True if commissionCount[0] > 0 else False
        comistion = Commission.objects.create(salesId=user,salesGun=salesGunFalg,sellCount=commissionCount[2],commission=commissionCount[0])
        comistion.save()
        return render(request,"salesPersonClear.html",{
            "date":comistion.commiDate,
            "newClearing":True,
            "totalSale":commissionCount[2],
            "commistion":commissionCount[0],
            "totalCount":totalCount
        })
    except Exception as e:
        print(e)
        return render(request, 'failure.html', {'reason': str(e)})

@login_required(login_url='/',)
def getAdmin(request):
    return render(request,"adminTemplates/adminPage.html",{"aliasname":request.user.aliasName})


def getUserCommissionTable(request,year,month):

    commissions = Commission.objects.filter(commiDate__year=year,commiDate__month=month)
    if month == 12:
        userParamDict = {"date_joined__lt": datetime.datetime(year + 1, 1, 1), "userType": "salesman"}
    else:
        userParamDict = {"date_joined__lt": datetime.datetime(year, month + 1, 1), "userType": "salesman"}
    users = User.objects.filter(**userParamDict).values("aliasName")
    tableRows =[]
    usernames = []
    for commission in commissions:
        temp ={}
        if commission.salesGun==True:
            temp['state'] = 1
        else:
            temp["state"] = 0
        temp["name"] = str(commission.salesId)
        temp['salecount'] = commission.sellCount
        usernames.append(temp["name"])
        tableRows.append(temp)

    for username in users:
        aliasname = username['aliasName']
        if aliasname not in usernames:
            tempDict ={"state":2,"name":aliasname,"salecount":0}
            tableRows.append(tempDict)
    return render(request,"adminTemplates/userCommissionMonth.html",{"tablerows":tableRows,"year":year,"month":month})
def userStatistical(request):

    dataDict = getUser()
    imageData,salesUsers = dataDict['imagedata'],dataDict['salesUsers']
    respDict = {"imagedata":imageData,"error":0,"title":"销售人员统计图","errorReason":"None"}
    return JsonResponse(respDict)


def productStatistical(request,year,month):
    return getJsonByMonth(year,month,saleProduct)

def productTownStatisticalMonth(request,year,month):
    return getJsonByMonth(year,month,townProduct)

def commissionStatisticalMonth(request,year,month):
    return getJsonByMonth(year,month,getUserCommisstionHistogram)

def commissionLine(request,year,month):
    now_time = datetime.datetime.now()
    if year > now_time.year:
        return JsonResponse({"error": 1, "errorReason": "年份超前"})
    if year==now_time.year:
        dataDict = getUserlineChar(now_time,"commission")
    else:
        dataDict = getUserlineChar(datetime.datetime(year,12,1),"commission")
    if dataDict['error']:
        return render(request, "failure.html", {"reason": "非法请求"})
    imageData = dataDict["imagedata"]
    returnDict = {"imagedata": imageData, "error": 0, "title": "佣金走势图", "errorReason": "None"}
    return JsonResponse(returnDict)

def saleCountLine(request,year,month):
    now_time = datetime.datetime.now()
    if year > now_time.year:
        return JsonResponse({"error": 1, "errorReason": "年份超前"})
    if year==now_time.year:
        dataDict = getUserlineChar(now_time,"sellCount")
    else:
        dataDict = getUserlineChar(datetime.datetime(year,12,1),"sellCount")
    if dataDict['error']:
        return JsonResponse({"error":1,"errorReason":"画图错误"})
    imageData = dataDict["imagedata"]
    returnDict = {"imagedata": imageData, "error": 0, "title": "总销售额走势图", "errorReason": "None"}
    return JsonResponse(returnDict)

def getPassHistogram(request,year,month):
    return getJsonByMonth(year, month, getPassNumberHistogram)

def getUserLineSale(request,username):
    return getUserLine(username,"sellCount")

def getUserLineComm(request,username):
    return getUserLine(username, "commission")

def getUserLine(username,flag):
    now_time = datetime.datetime.now()
    user = User.objects.get(username=username)
    try:
        commission = Commission.objects.get(salesId=user,commiDate__year=now_time.year,commiDate__month=now_time.month)
        thisMonthFlag = True
    except ObjectDoesNotExist:
        thisMonthFlag = False
    if(not thisMonthFlag):
        now_time = datetime.datetime(now_time.year,now_time.month-1 if now_time!=1 else 1 ,now_time.day)
    dataDict = getUserCommissionLine(now_time,user,flag)
    if dataDict['error']:
        return JsonResponse({"error": 1, "errorReason": "画图错误"})
    imageData = dataDict["imagedata"]
    returnDict = {"imagedata": imageData, "error": 0, "title": "总销售额走势图", "errorReason": "None"}
    return JsonResponse(returnDict)

def getProductLineView(request,year,month):
    now_time =datetime.datetime.now()
    if year > now_time.year:
        return JsonResponse({"error": 1, "errorReason": "年份超前"})
    if year == now_time.year:
        paramYear,paramMonth = year,now_time.month
    else:
        paramYear, paramMonth = year, 12
    dataDict = productLine(paramYear,paramMonth)
    if dataDict['error']:
        return JsonResponse({"error":1,"errorReason":"画图错误"})
    imageData = dataDict["imagedata"]
    returnDict = {"imagedata": imageData, "error": 0, "title": "产品走势图", "errorReason": "None"}
    return JsonResponse(returnDict)




def getOrderTable(user):
    now_time = datetime.datetime.now()
    monthOrders = OrderDetail.objects.filter(orderId__salesId=user,orderId__date__month=now_time.month) \
        .select_related('orderId').values('product', 'orderId', 'number', 'orderId__city')
    orders = {}
    for monthOrder in monthOrders:
        if monthOrder['orderId'] not in orders.keys():
            orders[monthOrder['orderId']] = {}
            orders[monthOrder['orderId']]['city'] = monthOrder['orderId__city']
        orders[monthOrder['orderId']][monthOrder['product']] = monthOrder['number']
    orderTable = []
    for key, value in orders.items():
        orderTable.append(value)
    return orderTable

def calCommission(totalCount):
    flag = True
    sellPrice = 0.0
    for key in products:
        if totalCount[key]==0:
            flag=False
        else:
            sellPrice+=totalCount[key] * prices[key]
    if not flag or sellPrice <0:
        return (0,'0',sellPrice)
    else:
        if 0<sellPrice<=1000:
            return (sellPrice * 0.1,'10%',sellPrice)
        elif 1000<sellPrice<=1800:
            commission =  1000 * 0.1 + (sellPrice-1000) * 0.15
            return (commission,'15%',sellPrice)
        elif sellPrice > 1800:
            tempcommission = 1000 * 0.1 + (1800-1000) * 0.15 + (sellPrice-1800) * 0.2
            return (tempcommission,'20%',sellPrice)

def getJsonByMonth(year,month,func):
    now_time = datetime.datetime.now()
    if year > now_time.year or month > 12 or month < 0:
        return JsonResponse({"error": 1, "errorReason": "年份或月份错误"})
    if month == 0:
        flag = "year"
        now_time = datetime.datetime(year, 1, 1)
    else:
        flag = "month"
        now_time = datetime.datetime(year, month, 1)
    dataDict = func(now_time, flag)
    if dataDict['error']:
        return JsonResponse({"error": 1, "errorReason": "画图错误"})
    imageData = dataDict["imagedata"]
    respDict = {"imagedata": imageData, "error": 0, "title": "销售量图", "errorReason": "None"}
    return JsonResponse(respDict)



def count(sellPrice):
    if 0 < sellPrice <= 1000:
        return sellPrice * 0.1
    elif 1000<sellPrice<=1800:
        commission = 1000 * 0.1 + (sellPrice - 1000) * 0.15
        return commission
    elif sellPrice > 1800:
        tempcommission = 1000 * 0.1 + (1800 - 1000) * 0.15 + (sellPrice - 1800) * 0.2
        return tempcommission
