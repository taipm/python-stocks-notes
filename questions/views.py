from django.db import models
from questions.Stocks import STOCKS, get_stock_data_from_api
from questions.marketAnalysis import market_analysis_result
from questions.stockAnalysis import stock_analysis_result
from questions.crawler import getDetail, importData, getStockPrices, getStocks
from questions.marketData import getAllStockPrices
from typing import Text
from django.forms.forms import Form
from pages.views import searchView
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from main.models import (Comment, CommentForm, Question, Answer, QuestionForm, AnswerForm, CommentSerializer,
                        QuestionSerializer, AnswerSerializer, Vocabulary)
from django.core.paginator import Paginator
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import questions.teleBot as Bot

import matplotlib
matplotlib.use('TkAgg')

# vote_type could be 'upvote', 'downvote', or 'cancel_vote'
def updateVote(user, target, vote_type, question_or_answer):
    if question_or_answer == 'question':
        upvoted_targets = user.upvoted_questions
        downvoted_targets = user.downvoted_questions
    else:
        upvoted_targets = user.upvoted_answers
        downvoted_targets = user.downvoted_answers

    upvoted_targets.remove(target)
    downvoted_targets.remove(target)

    # if this is an upvote, add an upvote. otherwise, add a downvote.
    if vote_type == 'upvote':
        upvoted_targets.add(target)
    elif vote_type == 'downvote':
        downvoted_targets.add(target)

    target.update_points()
    return target.points

def answerVoteView(request, id):
    return voteView(request, id, 'answer')

def questionVoteView(request, id):
    return voteView(request, id, 'question')

def voteView(request, id, question_or_answer):
    current_user = request.user
    if question_or_answer == 'question':
        target = Question.objects.get(pk=id)
    else:
        target = Answer.objects.get(pk=id)
    
    if not current_user.is_authenticated:
        return HttpResponse('Not logged in', status=401)
    if current_user.id == target.user_id:
        return HttpResponseBadRequest('Same user')
    if request.method != 'POST':
        return HttpResponseBadRequest('The request is not POST')
    vote_type = request.POST.get('vote_type')
    points = updateVote(current_user, target, vote_type, question_or_answer)
    if question_or_answer == 'answer':
        target.user.update_points()
    return JsonResponse({'vote_type': vote_type, 'points': points})

def questionView(request, id):
    print(id)
    current_user = request.user
    question = Question.objects.get(pk=id)
    print(question)
    # answers = Answer.objects.filter(question_id=id).order_by('created')
    # answers_serialized = AnswerSerializer(answers, many=True).data
    # comments = []
    # for answer in answers:
    #     comments.extend(Comment.objects.filter(answer_id=answer.id))
    #     #print(comments)
    # for answer in answers_serialized:
    #     answer['upvoted'] = False
    #     answer['downvoted'] = False
    #     if not current_user.is_authenticated:
    #         pass
    #     elif current_user.upvoted_answers.filter(id=answer['id']).count() > 0:
    #         answer['upvoted'] = True
    #     elif current_user.downvoted_answers.filter(id=answer['id']).count() > 0:
    #         answer['downvoted'] = True
    
    # For the question
    upvoted = False
    downvoted = False
    asked_by_user = False

    if not current_user.is_authenticated:
        pass
    elif current_user.upvoted_questions.filter(id=question.id).count() > 0:
        upvoted = True
    elif current_user.downvoted_questions.filter(id=question.id).count() > 0:
        downvoted = True
    elif current_user.id == question.user_id:
        asked_by_user = True
    
    print(question.title)
    my_note = ""
    #stocks = STOCKS.split(",")
    #print(stocks)
    # if len(str(question.title) in stocks:
    #     data = get_stock_data_from_api(question.title)
    #     html_content = data.to_html()
    #     print(data)
    #     my_note = my_note + " là mã cổ phiếu yêu thích "
    
    # data = get_stock_data_from_api(question.title)
    # html_content = data.to_html()
    # print(data)
    html_content = ""
    my_note = my_note + " là mã cổ phiếu yêu thích "
    question.title = question.title
    #question.body = "content" #html_content
    html_graph = ""# data.plot(x='Close',y='Volume',kind = 'scatter')
    html_content = html_content + question.body
    # context = {'question': question, 'answers': answers, 'comments':comments,
    #            'current_user': current_user, 'points': question.points,
    #            'upvoted': upvoted, 'downvoted': downvoted,
    #            'asked_by_user': asked_by_user,
    #            'upvoted': upvoted, 'downvoted': downvoted,
    #            'answers_serialized': answers_serialized}
    context = {'question': question}
    
    return render(request, 'question.html', context)

def newView(request):
    current_user = request.user

    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse('account_signup'))

    if request.method != 'POST':
        render(request, 'new.html', {'current_user': current_user})
    
    form = QuestionForm(request.POST)
    if not form.is_valid() or current_user.points < 0:
        return render(request, 'new.html', {'current_user': current_user})
        
    q = Question(
        user_id = current_user.id,
        title = form.cleaned_data['title'],
        body = form.cleaned_data['body']
    )
    q.save()
    return HttpResponseRedirect('/')


def answerView(request, id):
    current_user = request.user

    if not current_user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    if not request.method == 'POST':
        return HttpResponseRedirect(f'/question/{id}')
    form = AnswerForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(f'/question/{id}')
    a = Answer(
        user_id = current_user.id,
        question_id = id,
        text = form.cleaned_data['text']
    )
    a.save()
    return HttpResponseRedirect(f'/question/{id}')

def myAnswersView(request):
    current_user = request.user
    answers = Answer.objects.filter(user_id = current_user.id).order_by('-created')
    answers_exist = len(answers) > 0
    paginator = Paginator(answers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'my_answers.html',
                    {'current_user': current_user,
                    'answers_exist': answers_exist,
                    'page_obj': page_obj})

def myWordsView(request):
    current_user = request.user
    questions = Vocabulary.objects.filter(user_id = current_user.id).order_by('-created')
    questions_exist = len(questions) > 0
    return render(request, 'my_words.html',
                  {'current_user': current_user, 'questions': questions,
                   'questions_exist': questions_exist})
    
def myQuestionsView(request):
    current_user = request.user
    questions = Question.objects.filter(user_id = current_user.id).order_by('-created')
    questions_exist = len(questions) > 0
    return render(request, 'my_questions.html',
                  {'current_user': current_user, 'questions': questions,
                   'questions_exist': questions_exist})
    
#TAIPM - UPDATE QUESTION
#Update: 15.09.2021
def update(request, id):
    current_user = request.user
    question = Question.objects.get(pk=id)
    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse('account_signup'))

    if request.method != 'POST':
        render(request, 'update.html', {'current_user': current_user})
    
    form = QuestionForm(request.POST)
   
    if not form.is_valid() or current_user.points < 0:
        return render(request, 'update.html', {'current_user': current_user})
    
    question.title = form.cleaned_data['title']
    question.body = form.cleaned_data['body']
    question.save()
    
    return HttpResponseRedirect('/')

def updateQuestion(request, id):
    current_user = request.user
    question = Question.objects.get(pk=id)
    return render(request, 'update.html',
                  {'current_user': current_user, 'question': question})
        
def viewAnswer(request, id):
    current_user = request.user
    answer = Answer.objects.get(pk=id)  # question_id
    question = Question.objects.get(pk=answer.question_id)
    return render(request, 'answer.html',
                  {'current_user': current_user, 'answer': answer, 'question':question})
    
def updateAnswer(request, id):
    current_user = request.user
    answer = Answer.objects.get(pk=id)
    return render(request, 'updateAnswer.html',
                  {'current_user': current_user, 'answer': answer})


def saveAnswer(request, id):
    current_user = request.user
    answer = Answer.objects.get(pk=id)
  
    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse('account_signup'))

    if request.method != 'POST':
        render(request, 'updateAnswer.html', {'current_user': current_user})
 
    form = AnswerForm(request.POST)
    if not form.is_valid() or current_user.points < 0:
        return render(request, 'updateAnswer.html', {'current_user': current_user})

    answer.text = form.data['text']
    answer.save()

    return HttpResponseRedirect('/')

def graph_money(y, nn, title):
    print('Đang chuẩn bị vẽ đồ thị')
    x = np.arange(100)

    fig = plt.figure()
    plt.plot(x, y)
    plt.plot(x, nn)
    plt.title(title + " : Biểu đồ dòng tiền")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def graph_prices(prices, title):
    print('Đang chuẩn bị vẽ đồ thị')
    x = np.arange(100)

    fig = plt.figure()
    plt.plot(x, prices)
    plt.title(title + " : Biểu đồ giá")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def graph_money_with_avg(y, title):
    print('Đang chuẩn bị vẽ đồ thị')
    x = np.arange(100)
    
    fig = plt.figure()
    plt.title(title + " : Biểu đồ dòng tiền")
    plt.plot(x, y)
   
    #Single moving average in pandas
    df_sma = y.rolling(window=4).mean()
    plt.plot(x, df_sma, label= "sma(4)")
    df_sma_5 = y.rolling(window=5).mean()
    plt.plot(x, df_sma_5, label= "sma(5)")
    df_sma_10 = y.rolling(window=10).mean()
    plt.plot(x, df_sma_10, label= "sma(10)")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data
def return_graph():
    x = np.arange(0, np.pi*3, .1)
    y = np.sin(x)

    fig = plt.figure()
    plt.plot(x, y)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def viewGraph(request):
    data_graph = return_graph()
    stocks = getStocks()
    data = []
    for stock in stocks:
        try:
            stock_prices = getStockPrices(stock)
            data.append(stock_prices.to_html())
        except:
            Bot.send_message("StockNote| " + stock + " chưa có trong Crawler")
    #html = data[0].to_html()
    context = {'graph':data_graph,'data':data}
    #context = {'graph':data_graph,'data':data,'str_html':html}
    
    return render(request, 'graph.html', context)


def viewMarket(request):
    data = getAllStockPrices()
    market_info = market_analysis_result()
    #market_info
    #01 - Vuot dinh
    context = {'data':market_info.to_html()}
    return render(request, 'market.html', context)

def search(request):
    "Search in question and answer with keyword"
    print('view search')
    keyword = "search word ..."
    return render(request, 'search.html', {'search':keyword})

#from django.shortcuts import render
def doSearch(request):
    "Search in question and answer with keyword"
    print("finding ...")
    #current_user = request.user
    form = Form(request.POST)
    ask = form.data['keywords']
    
    try:
        #Phân tích n = 10 phiên gần nhất
        data = stock_analysis_result(ask,10)
        df = data[18]
        df_money = (df["DC"]*df["KL"]*10000*100)/1000000000 #Tính theo đơn vị chục tỷ
        df_nn_money = (((df["NN Mua"]-df["NN Ban"])*df["DC"])
                       * 10000*100)/1000000000  # Tính theo đơn vị chục tỷ
        print(df_nn_money)
        #chart_money = graph_money(df_money, df_nn_money,data[0])
        #chart_prices = graph_prices(df['DC'], data[0])
        #chart_money2 = graph_money_with_avg(df_money, data[0])
        #print(chart_money)
        
        chart_path = '<img src="https://vip.cophieu68.vn/imagechart/candle/' + \
            ask.lower() + '.png" alt="" title=" aaa" border="0">'
            
        if(len(data[9]) > 100):
            Bot.send_message("StockNotes | " + data[0] + " | " +  str(data[2]))
            return render(request, 'stock_view.html', {'stock': data[0], 'n' : data[1], 'price':data[2], 'vol':data[3], 
                                                       'price_max': data[4], 'price_min': data[5],
                                                       'vol_max': data[6], 'vol_min': data[7], 
                                                       'vol_avg': "{:.2f}".format(data[8]),
                                                       'price_history': data[9],
                                                       'rate_price': "{:.2f}".format(data[10]), 
                                                       'rate_vol': "{:.2f}".format(data[11]),
                                                       'mark': "{:.2f}".format(data[12]),
                                                       'pivots': data[13],
                                                       'note' : data[14],
                                                       'note_price':data[15],
                                                       'margin_price_inday': float("{:.2f}".format(data[16])),
                                                       'margin_price_today': float("{:.2f}".format(data[17])),
                                                       'count_giam': data[19],
                                                       'margin_giam': float("{:.2f}".format(data[20])),
                                                       'count_tang': data[21],
                                                       'margin_tang': float("{:.2f}".format(data[22])),
                                                       'money':float("{:.2f}".format((data[2]*data[3]*10000*100)/1000000000)),
                                                       'chart_path':chart_path,
                                                       #'graph' : chart_money,
                                                       #'graph_prices' : chart_prices,
                                                       #'graph2' : chart_money2,
                                                       
                                                       })
    except:
        questions = Question.objects.filter(title__contains=ask)
        return render(request, 'my_questions.html',{'questions': questions})

def addComment(request, id):
    current_user = request.user
    print("add comment ...")
    print(id)
    answerId = id
    answer = Answer.objects.get(pk=answerId)
    
    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse('account_signup'))

    context = {'answer': answer,
               'current_user': current_user}
    return render(request, 'addComment.html', context)

def viewComment(request, id):
    current_user = request.user
    comment = Comment.objects.get(pk=id)

    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse('account_signup'))

    context = {'comment': comment,
               'current_user': current_user}
    return render(request, 'comment.html', context)

def viewUpdateComment(request, id):
    current_user = request.user
    comment = Comment.objects.get(pk=id)

    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse('account_signup'))

    context = {'comment': comment,
               'current_user': current_user}
    return render(request, 'updateComment.html', context)


def updateComment(request, id):
    current_user = request.user
    comment = Comment.objects.get(pk=id)

    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse('account_signup'))

    if request.method != 'POST':
        render(request, 'updateComment.html', {'current_user': current_user})

    form = CommentForm(request.POST)
    if not form.is_valid() or current_user.points < 0:
        return render(request, 'updateComment.html', {'current_user': current_user})

    try:
        comment.text = form.data['text']
        comment.save()
        Bot.send_message("StockNotes\nComment: " + comment.text)
    except:
        Bot.send_message("StockNotes: Có lỗi xảy ra khi cập nhật Comment")

    return HttpResponseRedirect('/')

def saveComment(request, id):
    current_user = request.user
    print("save cooomment ..")
    #answer = Answer.objects.get(pk=id)
    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse('account_signup'))

    if request.method != 'POST':
        render(request, 'addComment.html', {'current_user': current_user})

    form = CommentForm(request.POST)
    if not form.is_valid() or current_user.points < 0:
        return render(request, 'addComment.html', {'current_user': current_user})

    c = Comment(
        user_id=current_user.id,
        answer_id = id,
        text=form.data['text']
    )
    c.save()
    
    return HttpResponseRedirect('/')


def myCommentsView(request):
    current_user = request.user
    comments = Comment.objects.filter(
        user_id=current_user.id).order_by('-created')
    comments_exist = len(comments) > 0
    paginator = Paginator(comments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'my_comments.html',
                  {'current_user': current_user,
                   'answers_exist': comments_exist,
                   'page_obj': page_obj})

# def getStockPrice(stock):
    
