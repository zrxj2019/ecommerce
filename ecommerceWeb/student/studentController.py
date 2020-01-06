import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
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
        topics=section.topic_set.all()
        topic_detail_list=[]
        for t in topics:
            pathlist=list(t.pathlist_set.all().values())
            temp_dict={'topic':model_to_dict(t),'pathlist':pathlist}
            topic_detail_list.append(temp_dict)
        if len(topic_detail_list) > 0:
            return HttpResponse(json.dumps({
                "status": 100,
                "result": {'topics':topic_detail_list}
            }))
        else:
            return HttpResponse(json.dumps({
                "status": 200,
                "result": {"notification":"未查询到课程内容！请重试！"}
            }))
    else:
        return HttpResponse(json.dumps({
            "status": 200,
            "result":  {"notification":"系统错误！"}
        }))
