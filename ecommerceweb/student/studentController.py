import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

from ecommerceweb.models import TestRecord
from .. import models


############################学生在线学习##############################
def getChapters():
    chapters = models.Chapter.objects.all()
    return chapters


@csrf_exempt
def getSectionDetails(request):
    topics = None
    if request.method == 'POST':
        data = request.POST
        sectionid = data['sectionid']
        section = models.Section.objects.get(sectionid=sectionid)
        topics = section.topic_set.all()
        topic_detail_list = []
        for t in topics:
            pathlist = list(t.pathlist_set.all().values())
            temp_dict = {'topic': model_to_dict(t), 'pathlist': pathlist}
            topic_detail_list.append(temp_dict)
        if len(topic_detail_list) > 0:
            return HttpResponse(json.dumps({
                "status": 100,
                "result": {'section': model_to_dict(section), 'topics': topic_detail_list}
            }))
        else:
            return HttpResponse(json.dumps({
                "status": 100,
                "result": {'section': model_to_dict(section)}
            }))
    else:
        return HttpResponse(json.dumps({
            "status": 200,
            "result": {"notification": "系统错误！"}
        }))


@csrf_exempt
# 获取实验记录的信息
def get_experiment(request):
    if request.method == 'POST':
        studentid = request.session.get('userid')
        try:
            experiments = list(models.Experiment.objects.filter(student_id=studentid)
                               .values_list('experimentid','experimentname','experimentdeadline','experimentstatus'))
        except TestRecord.DoesNotExist:
            experiment_record_num = 0
        else:
            experiment_record_num = len(experiments)

        return HttpResponse(json.dumps({
            "status": 100,
            "result": {"experimentnum": experiment_record_num, "experiments": experiments}
        },cls=DjangoJSONEncoder))
    else:
        return HttpResponse(json.dumps({
            "status": 200,
            "result": {"notification": "系统错误！"}
        }))

@csrf_exempt
# 获取实验记录的信息
def get_experiment_info(request):
    if request.method == 'POST':
        data = request.POST
        experimentid = data['experimentid']
        studentid = request.session.get('userid')
        experiment_info = models.Experiment.objects.get(student_id=studentid,experimentid=experimentid)
        if experiment_info!=None:
            return HttpResponse(json.dumps({
                "status": 100,
                "result": {"experimentinfo": model_to_dict(experiment_info)}
            },cls=DjangoJSONEncoder))
        else:
            return HttpResponse(json.dumps({
                "status": 100,
                "result": {"experimentinfo": model_to_dict(experiment_info),'notification':'查询失败，请重试！'}
            }, cls=DjangoJSONEncoder))
    else:
        return HttpResponse(json.dumps({
            "status": 200,
            "result": {"notification": "系统错误！"}
        }))

