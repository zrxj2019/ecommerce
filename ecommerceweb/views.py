from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from ecommerceweb.models import User
from ecommerceweb.models import Test,TestRecord,Question,QuestionRecord,Notification
from . import models
from . import forms
import json
import random
import datetime
from .student import studentController


#***********************页面跳转相关***********************
def main_teacher(request):
    validate = loginValidator(request)
    if validate != None:
        return validate
    return render(request, 'teacher/teacherMain.html', {'username':request.session.get('username')})
def main_student(request):
    validate=loginValidator(request)
    if validate!=None:
        return validate
    student = models.Student.objects.get(studentid=request.session.get('userid'))
    TOTALTOPICS = 28
    study_progress = len(student.studied_topics.all())
    return render(request, 'student/studentMain.html', {'username':request.session.get('username'),
                                                        'total':TOTALTOPICS, 'study_progress':study_progress})
def user_info_student(request):
    validate = loginValidator(request)
    if validate != None:
        return validate
    return render(request, 'student/user.html', {'username':request.session.get('username')})

def student_online_learning(request):
    validate = loginValidator(request)
    if validate != None:
        return validate
    chapters=studentController.getChapters()
    return render(request,'student/onlinelearning.html',{'username':request.session.get('username'),'chapters':chapters},)

def student_experiment(request):
    validate = loginValidator(request)
    if validate != None:
        return validate
    return render(request, 'student/experiment.html',{'username':request.session.get('username')})
#***********************登录登出相关***********************
#登录验证器，验证是否登录
def loginValidator(request):
    print(request.session.get('is_login', None))
    print(request.session.get('userid'))
    if not request.session.get('is_login', None) and (request.session.get('userid')==None):
        return redirect('/login/')
    else:
        #登录了转发到对应主页面
        role=request.session.get('role')
        if role==0:
            if 'teacher' not in request.get_full_path_info():
                return redirect('/teacher/')
            else:
                return None
        elif role==1:
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
    if request.method=="POST":
        login_form=forms.LoginForm(request.POST)
        error="<h6>登录错误！</h6><span>请检查输入</span>"
        # 先验证验证码是否正确
        capt = request.POST.get('captcha',None)  # 用户提交的验证码
        key = request.POST.get('hashkey',None)  # 验证码答案
        if not jarge_captcha(capt, key):
            error = "<h6>登录错误！</h6><span>验证码错误</span>"
            return render(request, 'login.html', locals())
        else:
            cap = captcha()
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user=models.User.objects.get(username=username)
            except User.DoesNotExist:
                error ="<h6>登录错误！</h6><span>用户名不存在</span>"
                return render(request, 'login.html',locals())
            if user.password==password:
                request.session['role'] = user.role
                if user.role==0:#教师
                    teacher=models.Teacher.objects.get(teacherid=username)
                    request.session['is_login'] = True
                    request.session['userid'] = username
                    request.session['username'] = teacher.teachername
                    return redirect('/teacher/')
                elif user.role==1:#学生
                    student=models.Student.objects.get(studentid=username)
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
        login_form=forms.LoginForm()
        cap=captcha()
        return render(request,'login.html',locals())

#登出
def logout(request):
    loginValidator(request)
    request.session.flush()
    return redirect("/login/")
'''
验证码相关
'''
# 创建验证码
def captcha():
    hashkey = CaptchaStore.generate_key()   #验证码答案
    image_url = captcha_image_url(hashkey)  #验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha
#刷新验证码
def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')
# 验证验证码
def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            if get_captcha.response == captchaStr.lower():     # 如果验证码匹配
                return True
        except:
            return False
    else:
        return False


############################学生考试##################################
#跳转界面
def test_student(request):
    loginValidator(request)
    return render(request,'student/studentTest.html',{'username':request.session.get('username')})
#获取所有考试信息
@csrf_exempt
def get_test_record_student(request):
    studentid=request.session.get('userid')
    print(studentid)
    try:
        testrecords = list(models.TestRecord.objects.filter(student_id=studentid)
                           .values_list('recordid','test__testname','test__testtime','test__testscore','test__state','datetime','duration','state','score'))
    except TestRecord.DoesNotExist:
        testRecordNum=0
    else:
        testRecordNum=len(testrecords)
    print(testrecords)

    return HttpResponse(json.dumps({
        'testRecordNum':testRecordNum,
        'testrecords': testrecords
    }))
@csrf_exempt
def get_new_notification_student(request):
    studentid = request.session.get('userid')
    try:
        notifications = list(models.Notification.objects.filter(student_id=studentid,read=False).values())
    except Notification.DoesNotExist:
        notificationNum = 0
    else:
        notificationNum = len(notifications)
    print(notifications)
    return HttpResponse(json.dumps({
        'notificationNum': notificationNum,
        'notifications': notifications
    }))

@csrf_exempt
def study_compare_pay(request):
    studentid = request.session.get('userid')

    return render(request, 'student/compare_pay.html', {'data': request.session.get('username')})

@csrf_exempt
def study_pay(request):
    studentid = request.session.get('userid')

    return render(request, 'student/pay.html', {'data': request.session.get('username')})

@csrf_exempt
def start_test_student(request):
    recordId=request.POST.get('recordId')
    print(recordId)
    testRecord=models.TestRecord.objects.get(recordid=recordId)
    test=models.Test.objects.get(testid=testRecord.test_id)
    xzNum=test.xznum
    dxNum=test.dxnum
    pdNum=test.pdnum
    if testRecord.state == 0:
        models.TestRecord.objects.filter(recordid=recordId).update(state=1)
        if xzNum != 0:
            xzl = [i[0] for i in models.Question.objects.filter(questionType=0).values_list('questionid')]
            xzQuestionIdList = random.sample(xzl, xzNum)
            print(xzl)
            print(xzQuestionIdList)
            for questionId in xzQuestionIdList:
                models.QuestionRecord.objects.create(test_id=test.testid, question_id=questionId,
                                                     student_id=testRecord.student_id)
                # xzQRList = models.QuesionRecord.objects.filter(test_id=test.testid, student_id=testRecord.student_id,
                #                                                question__questionType=0)\
                #     .values_list('recordid','question__questionid',)
        if dxNum != 0:
            dxl = [i[0] for i in models.Question.objects.filter(questionType=1).values_list('questionid')]
            dxQuestionIdList = random.sample(dxl, dxNum)
            print(dxl)
            print(dxQuestionIdList)
            for questionId in dxQuestionIdList:
                models.QuestionRecord.objects.create(test_id=test.testid, question_id=questionId,
                                                     student_id=testRecord.student_id)
                # dxQRList = models.QuesionRecord.objects.filter(test_id=test.testid, student_id=testRecord.student_id,
                #                                                question__questionType=1)
        if pdNum != 0:
            pdl = [i[0] for i in models.Question.objects.filter(questionType=2).values_list('questionid')]
            pdQuestionIdList = random.sample(pdl, pdNum)
            print(pdl)
            print(pdQuestionIdList)
            for questionId in pdQuestionIdList:
                models.QuestionRecord.objects.create(test_id=test.testid, question_id=questionId,
                                                     student_id=testRecord.student_id)
                # pdQRList = models.QuesionRecord.objects.filter(test_id=test.testid, student_id=testRecord.student_id,
                #                                                question__questionType=2)
        # 设置已用时为0分0秒
        now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usedSeconds=0
        m, s = divmod(usedSeconds, 60)
        used=str(m)+':'+str(s)
        models.TestRecord.objects.filter(recordid=recordId).update(datetime=now,duration=used)
        print(now)
    # request.session['testRecordId'] = recordId
    return HttpResponse(json.dumps({
        'msg':'开始考试'
    }))
    # return render(request, 'student/exam.html', {'student': student, 'test': test, 'testRecord': testRecord,
    #                                      'xzQuestionList': xzQuestionList,
    #                                      'dxQuestionList': dxQuestionList,
    #                                      'pdQuestionList': pdQuestionList})

@csrf_exempt
def view_test_student(request):
    recordId=request.POST.get('recordId') #testrecrodid
    print(recordId)
    testRecord = models.TestRecord.objects.get(recordid=recordId)
    test = models.Test.objects.get(testid=testRecord.test_id)
    student = models.Student.objects.get(studentid=testRecord.student_id)
    questionIdList = [i[0] for i in models.QuestionRecord.objects
        .filter(test_id=test.testid, student_id=testRecord.student_id)
        .values_list('question_id')]
    print(questionIdList)
    curQuestion = models.Question.objects.get(questionid=questionIdList[0])
    content=[i[0] for i in models.QuestionRecord.objects
        .filter(test_id=test.testid, student_id=testRecord.student_id)
        .values_list('content')]
    print(content)
    allSeconds=test.testtime*60
    usedSeconds=int(testRecord.duration.split(':')[0])*60+int(testRecord.duration.split(':')[1])
    minute,second=divmod(allSeconds-usedSeconds,60)
    return render(request, 'student/exam.html', {'student': student, 'test': test, 'testRecord': testRecord,
                                                 'minute':minute,
                                                 'second':second,
                                                 'curQuestion':curQuestion,
                                                 'content':content,
                                                 'questionIdList':questionIdList})
@csrf_exempt
def save_content_student(request):
    testId=request.POST.get('testId')
    studentId=request.POST.get('studentId')
    questionId=request.POST.get('questionId')
    content=request.POST.get('content')
    question=models.Question.objects.get(questionid=questionId)
    if content==question.answer:
        models.QuestionRecord.objects.filter(test_id=testId,student_id=studentId,question_id=questionId).update(
            content=content,istrue=1)
    else:
        models.QuestionRecord.objects.filter(test_id=testId, student_id=studentId, question_id=questionId).update(
            content=content, istrue=0)
    return HttpResponse(json.dumps({
        'result': str(questionId)+'更新成功'
    }))
@csrf_exempt
def locate_question_student(request):
    questionId=request.POST.get('questionId')
    curQuestion = models.Question.objects.get(questionid=questionId)
    curQuestionDict={}
    curQuestionDict['questionid']=curQuestion.questionid
    curQuestionDict['question']=curQuestion.question
    curQuestionDict['a']=curQuestion.a
    curQuestionDict['b'] = curQuestion.b
    curQuestionDict['c'] = curQuestion.c
    curQuestionDict['d'] = curQuestion.d
    curQuestionDict['questionType'] = curQuestion.questionType
    return HttpResponse(json.dumps({
        'curQuestion': curQuestionDict
    }))
@csrf_exempt
def calculate_score_student(request):
    testRecordId=request.POST.get('testRecordId')
    testRecord=models.TestRecord.objects.get(recordid=testRecordId)
    test = models.Test.objects.get(testid=testRecord.test_id)
    # 计算得分
    isTrueList=[i[0] for i in models.QuestionRecord.objects.filter(test_id=testRecord.test,student_id=testRecord.student)
        .values_list('istrue')]
    print(isTrueList)
    score=0
    for isTrue in isTrueList:
        if isTrue== 1:
            score+=10
    print(score)
    testScore=test.testscore
    finalScore=round(score*100/testScore)
    models.TestRecord.objects.filter(recordid=testRecordId).update(state=2,score=finalScore)

    return HttpResponse(json.dumps({
        'msg': '考试提交成功，得分为：'+str(score)
    }))

@csrf_exempt
def end_test_student(request):
    return redirect('/student/test/')
@csrf_exempt
def save_test_student(request):
    return redirect('/student/test/')
@csrf_exempt
def reset_duration_student(request):
    testRecordId = request.POST.get('testRecordId')
    seconds = request.POST.get('seconds')
    testRecord = models.TestRecord.objects.get(recordid=testRecordId)
    test = models.Test.objects.get(testid=testRecord.test_id)
    # 计算已用时
    allSeconds = test.testtime * 60
    usedSeconds = allSeconds - int(seconds)
    m, s = divmod(usedSeconds, 60)
    used = str(m) + ':' + str(s)
    models.TestRecord.objects.filter(recordid=testRecordId).update(duration=used)
    return HttpResponse(json.dumps({
        'msg': '已用时更新为：'+used
    }))
@csrf_exempt
def check_old_notification_student(request):
    studentid = request.session.get('userid')
    oldNotifications=models.Notification.objects.filter(student_id=studentid,read=True)
    return render(request,'student/notificationOld.html',locals())

@csrf_exempt
def reset_notification_read_student(request):
    notificationId=request.POST.get('notificationId')
    models.Notification.objects.filter(notificationid=notificationId).update(read=True)
    return HttpResponse(json.dumps({
        'msg': '通知已读'
    }))

############################学生考试##################################

############################教师考试##################################
#跳转界面
def test_teacher(request):
    loginValidator(request)
    students = models.Student.objects.all()
    return render(request,'teacher/teacherTest.html',locals())
#获取所有考试信息
@csrf_exempt
def get_test_teacher(request):
    try:
        tests = list(models.Test.objects.all().values())
    except Test.DoesNotExist:
        testNum=0
    else:
        testNum=len(tests)
    return HttpResponse(json.dumps({
        'testNum':testNum,
        'tests': tests
    }))
#发布单个考试
@csrf_exempt
def publish_test_teacher(request):
    # if request.session.get('is_login', None):  # 不允许重复登录
    #     # 登录了转发到对应主页面
    #     role = request.session.get('role')
    #     if role == 0:
    #         return redirect('/teacher/')
    #     elif role == 1:
    #         return redirect('/student/')
    testName = request.POST.get('testname')
    testTime = int(request.POST.get('testtime'))
    message = request.POST.get('message')
    students = request.POST.getlist('students')
    xzNum = request.POST.get('xznum')
    dxNum = request.POST.get('dxnum')
    pdNum = request.POST.get('pdnum')
    testScore =int(xzNum)*10+int(dxNum)*10+int(pdNum)*10
    publisTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(students)
    notificationContent='已发布考试：'+testName+'，'+message+'。\n其他具体信息请在考试模块查看。'
    try:
        models.Test.objects.get(testname=testName)
    except Test.DoesNotExist:
        # 添加考试信息
        test = Test(testname=testName, testtime=testTime, state=0, xznum=xzNum, dxnum=dxNum, pdnum=pdNum,testscore=testScore)
        test.save()
        print(test)
        # 为每个学生创建考试记录、考试通知
        for studentid in students:
            testRecord = TestRecord(test_id=test.testid,student_id=studentid, state=0)
            testRecord.save()
            notification = Notification(read=False, content=notificationContent, time=publisTime,student_id=studentid)
            notification.save()
        result = "<h6>发布成功！</h6>"
    else:
        result = "<h6>发布错误！</h6><span>考试名称已存在</span>"
    return HttpResponse(json.dumps({
        'result':result
    }))

#查看某个考试学生考试情况
@csrf_exempt
def check_test_teacher(request):
    testId = request.POST.get('testid')
    testRecords = list(models.TestRecord.objects.filter(test_id=testId).values())
    return HttpResponse(json.dumps({
        'testRecords':testRecords
    }))

#结束某个考试
@csrf_exempt
def end_test_teacher(request):
    testId = request.POST.get('testid')
    models.Test.objects.filter(testid=testId).update(state=1)
    models.TestRecord.objects.filter(test_id=testId).exclude(state=2).update(score=0)
    result = "<h6>已结束！</h6>"
    tests = list(models.Test.objects.all().values())
    return HttpResponse(json.dumps({
        'result':result,
        'tests':tests
    }))
############################教师考试##################################

############################在线学习##################################

############################pixi测试##################################
def pay_pixi_test(request):
    loginValidator(request)
    return render(request,'student/paytech.html',{'username':request.session.get('username')})
############################pixi测试##################################





