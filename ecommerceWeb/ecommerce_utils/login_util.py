from django.shortcuts import redirect
from django.shortcuts import render
from .. import models
from .. import forms
from .captcha_util import captcha
from .captcha_util import jarge_captcha
from ..models import User


# ***********************登录登出相关***********************
# 登录验证器，验证是否登录
def loginValidator(request):
    print(request.session.get('is_login', None))
    print(request.session.get('userid'))
    if not request.session.get('is_login', None) and (request.session.get('userid') == None):
        return redirect('/login/')
    else:
        # 登录了转发到对应主页面
        role = request.session.get('role')
        if role == 0:
            if 'teacher' not in request.get_full_path_info():
                return redirect('/teacher/')
            else:
                return None
        elif role == 1:
            if 'student' not in request.get_full_path_info():
                return redirect('/student/')
            else:
                return None


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        # 登录了转发到对应主页面
        role = request.session.get('role')
        if role == 0:
            return redirect('/teacher/')
        elif role == 1:
            return redirect('/student/')
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        error = "<h6>登录错误！</h6><span>请检查输入</span>"
        # 先验证验证码是否正确
        capt = request.POST.get('captcha', None)  # 用户提交的验证码
        key = request.POST.get('hashkey', None)  # 验证码答案
        if not jarge_captcha(capt, key):
            error = "<h6>登录错误！</h6><span>验证码错误</span>"
            return render(request, 'login.html', locals())
        else:
            cap = captcha()
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(username=username)
            except User.DoesNotExist:
                error = "<h6>登录错误！</h6><span>用户名不存在</span>"
                return render(request, 'login.html', locals())
            if user.password == password:
                request.session['role'] = user.role
                if user.role == 0:  # 教师
                    teacher = models.Teacher.objects.get(teacherid=username)
                    request.session['is_login'] = True
                    request.session['userid'] = username
                    request.session['username'] = teacher.teachername
                    return redirect('/teacher/')
                elif user.role == 1:  # 学生
                    student = models.Student.objects.get(studentid=username)
                    request.session['is_login'] = True
                    request.session['userid'] = username
                    request.session['username'] = student.studentname
                    return redirect('/student/')
            else:
                error = "<h6>登录错误！</h6><span>密码错误</span>"
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())
    else:
        login_form = forms.LoginForm()
        cap = captcha()
        return render(request, 'login.html', locals())


# 登出
def logout(request):
    loginValidator(request)
    request.session.flush()
    return redirect("/login/")
