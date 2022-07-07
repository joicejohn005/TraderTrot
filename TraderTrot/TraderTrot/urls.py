"""TraderTrot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('blog/',views.blog),
    path('blogs/',views.blogs),
    path('blogdetails/<int:bid>',views.blogdetails),
    path('login',views.login),
    path('user_profile/',views.user_profile),
    
    
    path('register',views.register),
    path('checklogin',views.checklogin),
    path('newindex/',views.newindex),
    path('logout/',views.logout),
    # path('pswdreset/',views.pswdreset),
    # path('forgot/',views.forgot),

    #admin
    path('ad_ac_reg/',views.ad_ac_reg),
    path('ad_userManage/', views.ad_userManage),
    path('ad_acManage/', views.ad_acManage),
    path('ad_home/',views.ad_home),
    path('status/<int:sid>',views.status),
    path('status2/<int:sid>',views.status2),

    #user/trader
    path('user_reg',views.user_reg),
    path('user_home/',views.user_home),

    path('tradebook/',views.tradebook),
    path('csvd/',views.csvd),
    path('pdf/',views.pdf),
    path('addtrade/',views.addtrade),
    
    path('user_request/',views.user_request),
    path('user_reqmanage/',views.user_reqmanage),
    path('user_reqdetails/<int:id>',views.user_reqdetails),
    path('user_reqsolution/<int:id>',views.user_reqsolution),
    path('user_course/',views.user_course),
    path('course_details/<int:id>',views.course_details),
    path('course/',views.course),
    path('subscribe/<int:cid>',views.subscribe),
    
    path('invest_req/',views.invest_req),
    path('trade_req/',views.trade_req),
    path('tips_req/',views.tips_req),
    path('other_req/',views.other_req),

    path('deletereq/',views.deletereq),
    
    path('stock_prediction/',views.stock_prediction),
    path('plotly/',views.plot),

    path('tradestock/',views.tradestock),
    path('stockinfo/',views.stockinfo),
    path('stockanalysis/',views.stockanalysis),
    path('course/<int:cid>',views.course),

    # path('test/',views.test2),
    path('graphpage/',views.graphpage),
    path('prediction/<str:symbol>',views.prediction),

    #accademy
    path('ac_reg/',views.ac_reg),
    path('acc_addPackage/',views.acc_addPackage),
    path('acc_addTutors/',views.acc_addTutors),
    path('addTutors/',views.addTutors),
    path('addPackage/',views.addPackage),
    path('addcoursefe/',views.addcoursefe),
    path('acc_home/',views.acc_home),

    #tutor
    path('tu_addBlog/',views.tu_addBlog),
    path('tu_home/',views.tu_home),
    path('tu_addUnitChapter/<int:cid>',views.tu_addUnitChapter),
    path('tu_addUnitChap/',views.tu_addUnitChap),
    path('tu_addChap/',views.tu_addChap),
    
    path('tu_course/',views.tu_course),
    path('addblog/',views.addblog),
    path('tu_dbtlist/',views.tu_dbtlist),
    path('tu_dbtdetails/<int:id>',views.tu_dbtdetails),
    path('markview/<int:did>',views.markview),
    path('markpro/<int:did>',views.markpro),
    path('solution/',views.solution),

    #testing
    path('clipboard/',views.clipboard),

    #ajax Jquery
    path('search-company',csrf_exempt(views.search_company),name='search-company'),
    path('search-date',csrf_exempt(views.search_date),name='search-date'),
    path('search-trade',csrf_exempt(views.search_trade),name='search-trade'),
    path('subscribe-course',csrf_exempt(views.subscribe)),
    path('unsubscribe-course',csrf_exempt(views.unsubscribe)),
    path('subscribe-check',csrf_exempt(views.subscribecheck)),
    path('status-change',csrf_exempt(views.status_change)),
    path('status-unchange',csrf_exempt(views.status_unchange)),
    path('status-check',csrf_exempt(views.status_check)),

    path('uno',csrf_exempt(views.unocheck),name='uno'),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)