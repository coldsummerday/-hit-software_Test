import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models import Sum,Count
from sellsGun.models import *
import datetime
products = ['lock','barrel','stock']

plt.rcParams['font.sans-serif']=['SimHei']

import numpy
def getUser():
    plt.close()
    salesUsers = User.objects.filter(userType='salesman').values_list("username","aliasName")
    bossUsers = User.objects.filter(userType="boss").values_list("username","aliasName")
    name_list = ["bossnumber","salesnumber"]
    number_list = [len(bossUsers),len(salesUsers)]
    plt.bar(range(len(number_list)),number_list,color="rgb",tick_label=name_list)
    for a, b in zip(range(len(number_list)), number_list):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.title("人员柱状图")
    plt.xlabel("人员类型")
    plt.ylabel("数量")
    sio = BytesIO()
    plt.savefig(sio,format="png")

    data = base64.encodebytes(sio.getvalue()).decode()
    return {"imagedata":data,"salesUsers":salesUsers}

def saleProduct(time,flag):
    plt.close()
    if flag=="year":
        paramDict = {"orderId__date__year":time.year}
        title = str(time.year)+"年"

    elif flag =="month":
        paramDict = {"orderId__date__year": time.year,"orderId__date__month":time.month}
        title = str(time.year) + "年"+str(time.month)+"月"

    else:
        return {"error":True}
    totalOrder = OrderDetail.objects.filter(**paramDict).values(
        'product').annotate(count=Sum('number'))
    totalCount = {eachDict['product']: eachDict['count'] for eachDict in totalOrder}
    for key in products:
        if key not in totalCount:
            totalCount[key] = 0
    xlabel = ["lock","barrel","stock"]
    number_list = [totalCount["lock"],totalCount["barrel"],totalCount["stock"]]
    plt.bar(range(len(number_list)), number_list, color="rgb", tick_label=xlabel)
    for a, b in zip(range(len(number_list)), number_list):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.title(title+"产品销售图")
    plt.xlabel("产品")
    plt.ylabel("数量")
    sio = BytesIO()
    plt.savefig(sio, format="png")
    data = base64.encodebytes(sio.getvalue()).decode()
    return {"imagedata": data,"error":False}

def townProduct(time,flag):
    plt.close()
    titles = []
    towns = ["北京","哈尔滨","上海","深圳"]
    aliatonws = ["Beijing","Haerbin","Shanghai","Shenzhen"]
    if flag!="year" and flag !="month":
        return {"error":True}
    bastDict={}
    if flag == "year":
        titles.extend([str(time.year),"年"])
        bastDict = {"orderId__date__year":time.year}
    elif flag=="month":
        titles.extend([str(time.year),"年",str(time.month),"月"])
        bastDict={"orderId__date__month":time.month,"orderId__date__year":time.year}
    townProducts={}
    for town in towns:
        paramDict = {"orderId__city":town}
        paramDict.update(bastDict)
        totalOrder = OrderDetail.objects.filter(**paramDict).values(
            'product').annotate(count=Sum('number'))
        totalCount = {eachDict['product']: eachDict['count'] for eachDict in totalOrder}
        for key in products:
            if key not in totalCount:
                totalCount[key] = 0
        townProducts[town] = totalCount
    locks = []
    barrels =[]
    stocks = []
    for town in towns:
        locks.append(townProducts[town]['lock'])
        barrels.append(townProducts[town]['barrel'])
        stocks.append(townProducts[town]['stock'])
    total_width, n = 0.8, 4
    width = total_width / n
    xlist = list(range(len(towns)))
    plt.bar(xlist,locks,width=width,label="lock",fc="r",tick_label=aliatonws)
    for a, b in zip(xlist, locks):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    for i in range(len(xlist)):
        xlist[i] +=width
    plt.bar(xlist, stocks, width=width, label="stock", fc="g",tick_label=aliatonws)
    for a, b in zip(xlist, stocks):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    for i in range(len(xlist)):
        xlist[i] +=width
    plt.bar(xlist, barrels, width=width, label="barrel", fc="b",tick_label=aliatonws)
    for a, b in zip(xlist, barrels):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.legend(loc="upper left")
    titles.append("产品销售地图")
    plt.title("".join(titles))
    plt.xlabel("销售地")
    plt.ylabel("销售量")
    sio = BytesIO()
    plt.savefig(sio, format="png")
    data = base64.encodebytes(sio.getvalue()).decode()
    return {"imagedata": data, "error": False}



def getUserCommisstionHistogram(time,flag):
    plt.close()
    if flag!="year" and flag !="month":
        return {"error":True}
    bastDict={}
    if flag == "year":
        bastDict = {"commiDate__year":time.year}
    elif flag=="month":
        bastDict={"commiDate__month":time.month,"commiDate__year":time.year}

    salesUsers = User.objects.filter(userType='salesman')
    xlabel = [user.aliasName for user in salesUsers]

    commisions = Commission.objects.filter(**bastDict).values('commission','salesId_id__aliasName')
    personCommissions = {commision['salesId_id__aliasName']:commision['commission'] for commision in commisions}
    commisionNumbers = []
    for aliasname in xlabel:
        if aliasname not in personCommissions.keys():
            commisionNumbers.append(0)
            personCommissions[aliasname] = -1
        else:
            commisionNumbers.append(personCommissions[aliasname])
    plt.bar(range(len(commisionNumbers)), commisionNumbers, color="rgb", tick_label=xlabel)
    for a,b in zip(range(len(xlabel)),commisionNumbers):
        text = "%.0f" % b if personCommissions[xlabel[a]]!=-1 else " "

        plt.text(a, b + 0.05, text, ha='center', va='bottom', fontsize=7)
    plt.legend(loc="upper left")
    sio = BytesIO()
    plt.savefig(sio, format="png")
    data = base64.encodebytes(sio.getvalue()).decode()
    return {"imagedata": data, "error": False}


def getUserCommissionLine(now_time,user,flag):
    plt.close()
    monthlist = range(1, now_time.month + 1)
    commisions = Commission.objects.filter(commiDate__year=now_time.year,salesId=user).values( flag,"commiDate")
    count=[]
    for commision in commisions:
        for month in monthlist:
            if month == commision['commiDate'].month:
                count.append(commision[flag])
            else:
                count.append(0)
    plt.plot(list(monthlist),count)
    for i, j in list(zip(list(monthlist), count)):
        plt.text(i, j + 1, j, fontsize=8)
    plt.legend(loc="upper left")
    plt.xticks(monthlist)
    plt.title(user.aliasName+flag)
    plt.xlabel(u'月份')
    plt.ylabel(u'数额')
    sio = BytesIO()
    plt.savefig(sio, format="png")
    data = base64.encodebytes(sio.getvalue()).decode()
    return {"imagedata": data, "error": False}
def getUserlineChar(now_time,flag):
    '''
    :param flag: 佣金commission或者销售额sellCount
    :return:
    '''
    plt.close()
    monthlist = range(1,now_time.month+1)
    if (len(monthlist)==0) or flag not in ["commission","sellCount"]:
        return {"error":True}
    salesUsers = User.objects.filter(userType='salesman')
    aliasnames = [user.aliasName for user in salesUsers]
    linesDict = {x:[] for x in aliasnames}

    commisions = Commission.objects.filter(commiDate__year=now_time.year).values(flag, 'salesId_id__aliasName',"commiDate")
    for commision in commisions:
        for month in monthlist:
            if month == commision['commiDate'].month:
                linesDict[commision['salesId_id__aliasName']].append(commision[flag])
            else:

                linesDict[commision['salesId_id__aliasName']].append(0)
    for x in aliasnames:
        if len(linesDict[x])==0:
            linesDict[x] = [0.0 for i in monthlist]

    for x in aliasnames:
        plt.plot(list(monthlist),linesDict[x],label=x)
        for i, j in list(zip(list(monthlist), linesDict[x])):
            plt.text(i, j + 1, j, fontsize=8)
    plt.legend(loc="upper left")
    plt.xticks(monthlist)
    plt.title(flag)
    plt.xlabel(u'月份')
    plt.ylabel(u'数额')
    sio = BytesIO()
    plt.savefig(sio, format="png")
    data = base64.encodebytes(sio.getvalue()).decode()
    return {"imagedata": data, "error": False}

def getPassNumberHistogram(now_time,flag):
    year = now_time.year
    month = now_time.month

    monthlist = range(1, month + 1)
    aliasmonth = [str(x)+"月" for x in monthlist]
    totalPersonNumber = []
    passPersonNumber = []
    for eachMonth in monthlist:
        if eachMonth==12:
            userParamDict = {"date_joined__lt": datetime.datetime(year+1, 1, 1), "userType": "salesman"}
        else:
            userParamDict = {"date_joined__lt": datetime.datetime(year, eachMonth+1, 1), "userType": "salesman"}
        totalPersonNumber.append(len(User.objects.filter(**userParamDict)))
        commissionParamDict = {"commiDate__year":year,"commiDate__month":eachMonth,"salesGun":True}
        passUsers = Commission.objects.filter(**commissionParamDict).values_list("commission","salesId_id__aliasName")
        passNumber = len(passUsers)
        passPersonNumber.append(passNumber)
    total_width, n = 0.6, 2
    width = total_width / n
    monthlist = list(monthlist)
    plt.close()
    plt.bar(monthlist, totalPersonNumber, width=width, label="totalnumber", fc="r", tick_label=aliasmonth)
    for a, b in zip(monthlist, totalPersonNumber):
        plt.text(a, b + 0.05, '%d' % b, ha='center', va='bottom', fontsize=7)
    for i in range(len(monthlist)):
        monthlist[i] += width
    plt.bar(monthlist, passPersonNumber, width=width, label="passnumber", fc="g", tick_label=aliasmonth)
    for a, b in zip(monthlist, passPersonNumber):
        plt.text(a, b + 0.05, '%d' % b, ha='center', va='bottom', fontsize=7)
    plt.legend(loc="upper left")
    plt.title("达到奖金人数图")
    plt.xlabel("月份")
    plt.ylabel("人数")
    sio = BytesIO()
    plt.savefig(sio, format="png")
    data = base64.encodebytes(sio.getvalue()).decode()
    return {"imagedata": data, "error": False,}


def productLine(year,month):
    plt.close()
    now_time = datetime.datetime.now()
    if year > now_time.year or (year==now_time.year and month > now_time.month) or month >12 or month<1:
        return {"error": True}
    monthlist = range(1, month + 1)
    aliasmonth = [str(x) + "月" for x in monthlist]
    productListDict ={product:[] for product in products}
    for eachMonth in monthlist:
        bastDict = {"orderId__date__month": eachMonth, "orderId__date__year": year}
        totalOrder = OrderDetail.objects.filter(**bastDict).values(
            'product').annotate(count=Sum('number'))
        if len(totalOrder)==0:
            for key,value in productListDict.items():
                value.append(0.0)
        else:
            totalCount = {eachDict['product']: eachDict['count'] for eachDict in totalOrder}
            for key,value in totalCount.items():
                productListDict[key].append(value)

    for key,value in productListDict.items():
        plt.plot(list(monthlist),value,label=key)
        for i,j in zip(list(monthlist),value):
            plt.text(i,j+1,j,fontsize=8)
    plt.legend(loc="upper left")
    title = [str(year),"年1月到",str(month),"月各个零件销售曲线图"]
    plt.title("".join(title))
    plt.xticks(monthlist)
    plt.xlabel("月份")
    plt.ylabel("销售额")
    sio = BytesIO()
    plt.savefig(sio, format="png")
    data = base64.encodebytes(sio.getvalue()).decode()
    return {"imagedata": data, "error": False}











    
    





























