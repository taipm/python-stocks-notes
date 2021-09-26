import django
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from collections import UserList
from django.db import models
from django.db.models.base import Model
from pandas.core.arrays.categorical import contains
from main.models import (Comment, CommentForm, Question, Answer, QuestionForm, AnswerForm, CommentSerializer,
                         QuestionSerializer, AnswerSerializer)
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas
from pytz import UTC
import questions.teleBot as Bot
sched = BlockingScheduler()
import datetime
from questions.crawler import importData
import time

print('Schedule')
@sched.scheduled_job('interval', minutes=5, timezone=UTC)

def timed_job():
    print('Schedule')
    now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    STOCK = 'HPG'
    df = importData(STOCK)
    rs = pandas.DataFrame(df).to_markdown()
    Bot.send_message('Trong giờ : ' + now)
    createOrUpdatePost()
    #Bot.send_message(STOCK + rs)

def createOrUpdatePost():
    today = datetime.datetime.now().strftime("%m/%d/%Y")
    print(today)
  
    q = Question.objects.filter(title__contains=today)
    title = "Marrket | " + today
    
    if(len(q) >= 1):
        print(q[0])
    else:
        print('Không có em nào')
        print(title)
        createQuestion(title, "HPG")
    
#sched.start()
def createQuestion(title, body):
    User = get_user_model()
    users = User.objects.all()
    #print(users[0].id)
    q = Question(
        user_id=users[0].id,
        title=title,
        body=body
    )
    #print(q)
    q.save()
