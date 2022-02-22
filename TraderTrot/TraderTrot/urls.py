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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('blog/',views.blog),
    path('blogs/',views.blogs),
    path('login',views.login),
    
    
    path('register',views.register),
    path('checklogin',views.checklogin),
    path('newindex/',views.newindex),
    path('logout/',views.logout),

    #admin
    path('ad_ac_reg/',views.ad_ac_reg),
    path('ad_userManage/', views.ad_userManage),
    path('ad_acManage/', views.ad_acManage),
    path('ad_home/',views.ad_home),

    #user/trader
    path('user_reg',views.user_reg),
    path('tradebook/',views.tradebook),
    path('user_home/',views.user_home),
    path('addtrade/',views.addtrade),

    #accademy
    path('ac_reg/',views.ac_reg),
    path('acc_addPackage/',views.acc_addPackage),
    path('acc_addTutors/',views.acc_addTutors),
    path('addTutors/',views.addTutors),
    path('addPackage/',views.addPackage),
    path('acc_home/',views.acc_home),

    #tutor
    path('tu_addBlog/',views.tu_addBlog),
    path('tu_home/',views.tu_home),
    path('addblog/',views.addblog),

    #testing
    path('clipboard/',views.clipboard),
    path('plotly/',views.plot)

]