from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
import json
from ecommerceweb.models import TestRecord
from .. import models
from ..ecommerce_utils.login_util import loginValidator


############################教师页面跳转##############################
# 页面跳转
def student_progress(request):
    validate = loginValidator(request)
    if validate != None:
        return validate
    return render(request, 'teacher/learningprogress.html', {'username': request.session.get('username')})


@csrf_exempt
# 获得所有学生学习进度
def get_all_student_progress(request):
    if request.method == 'POST':
        # 获取所有学生，计算每个学生的学习进度
        students = models.Student.objects.all()
        student_list = []
        for s in students:
            s_dict = model_to_dict(s)
            s_dict.pop('password')
            s_dict['study_num'] = len(s.studied_section.all())
            student_list.append(s_dict)
        return HttpResponse(json.dumps({
            "status": 100,
            "result": {'student_list': student_list}
        }, cls=DjangoJSONEncoder))
    else:
        return HttpResponse(json.dumps({
            "status": 200,
            "result": {"notification": "系统错误！"}
        }))
