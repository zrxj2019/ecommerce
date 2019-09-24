from django.db import models

class User(models.Model):
    roleTuple = (
        (0, "teacher"),
        (1, "student"),
    )
    username=models.CharField(max_length=15,primary_key=True,unique=True)
    password=models.CharField(max_length=45)
    role=models.IntegerField(choices=roleTuple)

class Teacher(models.Model):
    teacherid=models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
    teachername=models.CharField(max_length=45)


class Student(models.Model):
    studentid=models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
    studentname=models.CharField(max_length=45)