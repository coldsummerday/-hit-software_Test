
from django.urls import path
from .views import *

urlpatterns = [
    path('',LoginView.as_view(),name ='home'),
    path('login/',LoginView.as_view(),name="mylogin"),
    path('register/', do_register, name='register'),
    path('addOrder/',addOrder,name="addOrder"),
    path("addClearOrder/",clearingCommission,name="addClearing"),
    path("pageadmin/",getAdmin,name="pageadmin"),
    path('statistical/user',userStatistical,name="userStatistical"),
    path('statistical/product/month/<int:year>/<int:month>',productStatistical,name="productStatistical"),
    path('statistical/product/town/month/<int:year>/<int:month>', productTownStatisticalMonth, name="productTownStatisticalMonth"),
    path('statistical/user/commission/histogram/<int:year>/<int:month>',commissionStatisticalMonth,name="commissionStatisticalMonth"),
    path('statistical/user/commission/line/<int:year>/<int:month>',commissionLine,name="commissionLine"),
    path('statistical/user/sellcount/line/<int:year>/<int:month>',saleCountLine,name="salecountline"),
    path('statistical/user/pass/<int:year>/<int:month>',getPassHistogram,name="getPassHistogram"),
    path('statistical/product/line/<int:year>/<int:month>',getProductLineView,name="getProductLineView"),
    path('statistical/table/passuser/<int:year>/<int:month>',getUserCommissionTable),
    path('statistical/user/commission/<str:username>',getUserLineComm),
    path('statistical/user/sell/<str:username>',getUserLineSale),

]

