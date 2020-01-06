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
from ecommerceWeb.student import studentController
from django.contrib import admin
from django.urls import include

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
urlpatterns = [
    path('control/', admin.site.urls),  # 管理员访问路径 127.0.0.1:8000/control
    # ***********登录、登出*************
    path('login/', views.login),
    path('captcha/', include('captcha.urls')),
    path('refresh_captcha/', views.refresh_captcha),
    path('logout/', views.logout),
    # ***********学生*******************
    path('student/', views.main_student),
    path('student/user/', views.user_info_student),
    path('student/test/', views.test_student),
    path('student/test/get_test_record/', views.get_test_record_student),
    path('student/test/start_test/', views.start_test_student),
    path('student/test/view_test/', views.view_test_student),
    path('student/test/view_test/save_content/', views.save_content_student),
    path('student/test/view_test/locate_question/', views.locate_question_student),
    path('student/test/view_test/calculate_score/', views.calculate_score_student),
    path('student/test/view_test/end_test/', views.end_test_student),
    path('student/test/view_test/save_test/', views.save_test_student),
    path('student/test/view_test/reset_duration/', views.reset_duration_student),
    path('student/get_new_notifications/', views.get_new_notification_student),
    # 在各种界面获取新通知
    path('student/test/get_new_notifications/', views.get_new_notification_student),
    path('student/notifications/get_new_notifications/', views.get_new_notification_student),
    # 在各种界面更新通知已读
    path('student/test/reset_notification_read/', views.reset_notification_read_student),
    path('student/notifications/', views.check_old_notification_student),

    # ****在线学习模块****#
    path('student/onlinelearning/', views.student_online_learning),
    path('student/onlinelearning/get_section_details', studentController.getSectionDetails),
    # ***********教师*******************
    path('teacher/', views.main_teacher),
    path('teacher/test/', views.test_teacher),
    path('teacher/test/get_test/', views.get_test_teacher),
    path('teacher/test/publish_test/', views.publish_test_teacher),
    path('teacher/test/check_test/', views.check_test_teacher),
    path('teacher/test/end_test/', views.end_test_teacher)

]
