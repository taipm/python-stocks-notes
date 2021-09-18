from questions.crawler import getDetail
from typing import Text
from django.forms.forms import Form
from pages.views import searchView
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from main.models import (Comment, CommentForm, Question, Answer, QuestionForm, AnswerForm, CommentSerializer,
                        QuestionSerializer, AnswerSerializer)
from django.core.paginator import Paginator

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
    current_user = request.user
    question = Question.objects.get(pk=id)
    answers = Answer.objects.filter(question_id=id).order_by('created')
    answers_serialized = AnswerSerializer(answers, many=True).data
    for answer in answers_serialized:
        answer['upvoted'] = False
        answer['downvoted'] = False
        if not current_user.is_authenticated:
            pass
        elif current_user.upvoted_answers.filter(id=answer['id']).count() > 0:
            answer['upvoted'] = True
        elif current_user.downvoted_answers.filter(id=answer['id']).count() > 0:
            answer['downvoted'] = True
    
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
        
    context = {'question': question, 'answers': answers,
               'current_user': current_user, 'points': question.points,
               'upvoted': upvoted, 'downvoted': downvoted,
               'asked_by_user': asked_by_user,
               'upvoted': upvoted, 'downvoted': downvoted,
               'answers_serialized': answers_serialized}
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

def search(request):
    "Search in question and answer with keyword"
    print('view search')
    keyword = "search word ..."
    return render(request, 'search.html', {'search':keyword})


def doSearch(request):
    "Search in question and answer with keyword"
    print("finding ...")
    #current_user = request.user
    form = Form(request.POST)
    # print(form.data)
    # print(form.data['keywords'])
    ask = form.data['keywords']
    
    if(ask == "HPG"):
        data = getDetail("HPG")
        return render(request, 'stock_view.html', {'data': data})
    
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
    
