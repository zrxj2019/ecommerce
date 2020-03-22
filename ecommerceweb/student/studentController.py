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
        # 查询所有模拟测试
        section_simulations = section.sectionsimulation_set.all()
        section_simulation_list = []
        for ss in section_simulations:
            section_simulation_answer = list(ss.sectionsimulationanswer_set.all().values())
            temp_dict = {'section_simulation': model_to_dict(ss), 'answers': section_simulation_answer}
            section_simulation_list.append(temp_dict)
        # 问题
        section_questions = list(section.sectionquestion_set.all().values())
        studentid = request.session.get('userid')
        # 查询当前学习时间
        current_progress, created = models.Progress.objects.get_or_create(student_id=studentid,
                                                                          section_id=sectionid,
                                                                          defaults={'duration': 0, 'isfinish': 0,
                                                                                    'content': '未完成'},
                                                                          )
        section_dict = model_to_dict(section)
        section_dict.pop('students')
        section_dict.pop('teachers')
        current_duration = current_progress.duration
        if len(topic_detail_list) > 0:
            return HttpResponse(json.dumps({
                "status": 100,
                "result": {'section': section_dict, 'topics': topic_detail_list,
                           'sectionsimulations': section_simulation_list, 'sectionquestions': section_questions,
                           'current_duration': current_duration
                           }
            }))
        else:
            return HttpResponse(json.dumps({
                "status": 100,
                "result": {'section': section_dict,
                           'current_duration': current_duration
                           }
            }))
    else:
        return HttpResponse(json.dumps({
            "status": 200,
            "result": {"notification": "系统错误！"}
        }))


@csrf_exempt
# 更新学生的学习进度
def updateStudyProgress(request):
    if request.method == 'POST':
        data = request.POST
        sectionid = data['sectionid']
        duration = data['duration']
        studentid = request.session.get('userid')
        if int(duration) == 300:
            models.Progress.objects.filter(section_id=sectionid, student_id=studentid).update(duration=int(duration),
                                                                                              isfinish=1)
        else:
            models.Progress.objects.filter(section_id=sectionid, student_id=studentid).update(duration=int(duration))
        return HttpResponse(json.dumps({
            "status": 100,
            "result": {"notification": "更新时间完成！"}
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
                               .values_list('experimentid', 'experimentname', 'experimentdeadline', 'experimentstatus'))
        except TestRecord.DoesNotExist:
            experiment_record_num = 0
        else:
            experiment_record_num = len(experiments)

        return HttpResponse(json.dumps({
            "status": 100,
            "result": {"experimentnum": experiment_record_num, "experiments": experiments}
        }, cls=DjangoJSONEncoder))
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
        experiment_info = models.Experiment.objects.get(student_id=studentid, experimentid=experimentid)
        if experiment_info != None:
            return HttpResponse(json.dumps({
                "status": 100,
                "result": {"experimentinfo": model_to_dict(experiment_info)}
            }, cls=DjangoJSONEncoder))
        else:
            return HttpResponse(json.dumps({
                "status": 100,
                "result": {"experimentinfo": model_to_dict(experiment_info), 'notification': '查询失败，请重试！'}
            }, cls=DjangoJSONEncoder))
    else:
        return HttpResponse(json.dumps({
            "status": 200,
            "result": {"notification": "系统错误！"}
        }))

###########################对比不同运营方式##########################
