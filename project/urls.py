"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
"""
网址入口，关联到对应views.py中的一个函数
"""
from django.urls import path
# from django.conf.urls import url
from ecommerceWeb import views
from django.contrib import admin
from django.urls import include
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
urlpatterns = [
    path('control/', admin.site.urls), #管理员访问路径 127.0.0.1:8000/control
    #***********登录、登出*************
    path('login/', views.login),
    path('captcha/', include('captcha.urls')),
    path('refresh_captcha/',views.refresh_captcha),
    path('logout/', views.logout),
    #***********学生*******************
    path('student/', views.main_student),
    path('student/user/',views.user_info_student)
    #***********教师*******************
]