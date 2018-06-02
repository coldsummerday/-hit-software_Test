from django.db import models
from  django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    userType = models.CharField(max_length=20,choices=(('salesman',"销售员"),('boss','老板')),verbose_name="用户类型")
    aliasName = models.CharField(max_length=25,verbose_name="昵称",)
    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.aliasName
    def __unicode__(self):
        return self.aliasName


class Order(models.Model):
    salesId = models.ForeignKey(User,verbose_name="销售员",on_delete=models.CASCADE)
    city = models.CharField(max_length=10,verbose_name="销售城市")
    date = models.DateField(auto_now_add=True,verbose_name="销售日期")

    class Meta:
        verbose_name = "销售订单"
        verbose_name_plural = verbose_name
        ordering = ['-date']

class OrderDetail(models.Model):
    orderId = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=10,choices=(('lock',"枪锁"),('stock','枪托'),('barrel',"枪杆")),verbose_name="产品名称")
    number = models.IntegerField(verbose_name="销售数量")
    total = models.FloatField(verbose_name="销售总金额")

    class Meta:
        verbose_name = "销售订单详情"
        verbose_name_plural = verbose_name
        ordering = ['-orderId']


class Commission(models.Model):
    salesId = models.ForeignKey(User,verbose_name="销售员",on_delete=models.CASCADE)
    salesGun = models.BooleanField(verbose_name="是否卖出完整的枪?",default=False)
    commissionFlag = models.BooleanField(verbose_name="是否已经结账",default=True)
    commiDate = models.DateField(auto_now_add=True,verbose_name="结算日期")
    sellCount = models.IntegerField(verbose_name="销售额")
    commission = models.FloatField(verbose_name="提成")


