from django.db import models


# user表控制登陆登出
# 在mysql数据库中实现插入、修改、删除触发器确保user、teacher、student表的数据一致性
from django.utils import timezone


class User(models.Model):
    roleTuple = (
        (0, "teacher"),
        (1, "student"),
    )
    username = models.CharField(max_length=15, primary_key=True, unique=True)
    password = models.CharField(max_length=45,default=None)
    role = models.IntegerField(choices=roleTuple)


# 教师实体
class Teacher(models.Model):
    teacherid = models.CharField(max_length=15, primary_key=True)
    teachername = models.CharField(max_length=45)
    password = models.CharField(max_length=45,default=None)
    department = models.CharField(max_length=45,null=True)


class Student(models.Model):
    studentid = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=45,default=None)
    studentname = models.CharField(max_length=45)


# 课程实体，包括章、节、知识点、知识点的资源路径
class Chapter(models.Model):
    chapterid = models.AutoField(primary_key=True)
    chaptername=models.CharField(max_length=60,default=None)
    content = models.TextField(null=True)


class Section(models.Model):
    sectionid = models.AutoField(primary_key=True)
    sectionname=models.CharField(max_length=60,default=None)
    content = models.TextField(null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher, through='Statistic')

class SectionSimulation(models.Model):
    simulationid=models.AutoField(primary_key=True)
    simulationtype=models.IntegerField()
    simulationtitle=models.TextField()
    section=models.ForeignKey(Section, on_delete=models.CASCADE)

class SectionSimulationAnswer(models.Model):
    answerid = models.AutoField(primary_key=True)
    answertitle=models.TextField()
    content=models.TextField()
    sectionsimulation = models.ForeignKey(SectionSimulation, on_delete=models.CASCADE)

class SectionQuestion(models.Model):
    questionid=models.AutoField(primary_key=True)
    questiontitle=models.TextField()
    content=models.TextField()
    section=models.ForeignKey(Section, on_delete=models.CASCADE)

class Topic(models.Model):
    topicTuple = (
        (0, "normal"),
        (1, "media"),
    )
    topicid = models.AutoField(primary_key=True)
    topicname=models.CharField(max_length=60,default=None)
    content = models.TextField(null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    topictype=models.IntegerField(choices=topicTuple,default=0)
    students = models.ManyToManyField(Student, through='Progress')


class Pathlist(models.Model):
    pathType = (
        (0, "ppt"),
        (1, "jpg"),
        (2, "url"),
    )
    pathlistid = models.AutoField(primary_key=True)
    path = models.CharField(max_length=200)
    type = models.IntegerField(choices=pathType)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


# 教师、学生、知识点构成的多对多联关系，教师可以对某学生在某知识点的内容作出评价
class Comment(models.Model):
    comment = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.CharField(max_length=600)
    time = models.DateTimeField(auto_now=True)


# 教师和章节之间存在多对多的关系，用于显示章节的统计信息
class Statistic(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    score_avg = models.FloatField()
    # 已学习人数
    studentnum = models.IntegerField()

    class Meta:
        unique_together = ("teacher", "section")


# 管理员查看每天的登陆系统的人数
class Online(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    number = models.IntegerField()


# 学生会收到系统通知
class Notification(models.Model):
    notificationid = models.AutoField(primary_key=True)
    read = models.BooleanField(default=False)
    content = models.CharField(max_length=600)
    time = models.CharField(max_length=200)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


# 学生与知识点之间存在多对多关系
# progree用于查看学生的学习进程
class Progress(models.Model):
    student = models.ForeignKey(Student, related_name='studied_topics', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.CharField(null=True, max_length=200)

    class Meta:
        unique_together = ("student", "topic")


# 题库
class Question(models.Model):
    questionid = models.AutoField(primary_key=True)
    question = models.CharField(max_length=600)
    a = models.CharField(max_length=200)
    b = models.CharField(max_length=200)
    c = models.CharField(max_length=200)
    d = models.CharField(max_length=200)
    questionType = models.IntegerField()
    answer = models.CharField(max_length=200)


#考试
class Test(models.Model):
    testid = models.AutoField(primary_key=True)
    testname = models.CharField(max_length=200)
    testtime = models.IntegerField()
    state = models.IntegerField() #考试是否开放，0为正在开放，1为考试已结束
    xznum = models.IntegerField()
    dxnum = models.IntegerField()
    pdnum = models.IntegerField()
    testscore = models.IntegerField()

# 学生考试记录
class TestRecord(models.Model):
    recordid = models.AutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    datetime = models.CharField(max_length=200,null=True)
    duration = models.CharField(max_length=200,null=True)
    state = models.IntegerField()
    score = models.IntegerField(null=True)


# 学生答题记录
class QuestionRecord(models.Model):
    recordid = models.AutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.CharField(max_length=200,null=True)
    istrue = models.IntegerField(null=True)

# 学生提交实验
class Experiment(models.Model):
    experimentid=models.AutoField(primary_key=True)
    experimentname=models.CharField(max_length=200)
    content=models.TextField(null=True)
    experimentdeadline=models.DateField(default=timezone.now)
    experimentstatus=models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,default=None)


