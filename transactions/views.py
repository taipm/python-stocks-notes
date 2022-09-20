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
                        QuestionSerializer, AnswerSerializer, Transaction, Vocabulary)
from django.core.paginator import Paginator
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import questions.teleBot as Bot


def myTransactionsView(request):
    print("myTransactionsView")
    current_user = request.user
    print(current_user)
    transactions = Transaction.objects.filter(user_id = current_user.id).order_by('-created')
    print(transactions)
    transactions_exist = len(transactions) > 0
    print(transactions_exist)
    return render(request, 'my_transactions.html',
                  {'current_user': current_user, 'transactions': transactions,
                   'transactions_exist': transactions_exist})


def TransactionView(request, id):
    #print(id)
    current_user = request.user
    transaction = Transaction.objects.get(pk=id)
    print(transaction)
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
    
    if not current_user.is_authenticated:
        pass
    elif current_user.id == transaction.user_id:
        asked_by_user = True
    
    print(transaction.symbol)
    
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
    transaction.symbol = transaction.symbol
    #question.body = "content" #html_content
    
    #html_content = html_content + question.body
    # context = {'question': question, 'answers': answers, 'comments':comments,
    #            'current_user': current_user, 'points': question.points,
    #            'upvoted': upvoted, 'downvoted': downvoted,
    #            'asked_by_user': asked_by_user,
    #            'upvoted': upvoted, 'downvoted': downvoted,
    #            'answers_serialized': answers_serialized}
    context = {'transaction': transaction}
    
    return render(request, 'transaction.html', context)

