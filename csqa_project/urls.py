from django.contrib import admin
from django.urls import path, include
from main.views import homeFeedView, leaderboardView
from pages.views import aboutPageView
from questions.views import (addComment, questionView, saveComment, update, updateQuestion, newView, 
                            answerView, doSearch, search, myCommentsView, viewUpdateComment, updateComment,viewComment,
                            myQuestionsView, myWordsView ,myAnswersView, questionVoteView, viewMarket,                            
                            updateAnswer, saveAnswer, answerVoteView, viewAnswer, viewGraph)
from transactions.views import myTransactionsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeFeedView),
    #path('test/', testView),
    path('leaderboard/', leaderboardView),
    #path('search/', searchView, name='search'),
    path('search/', search, name='search'),
    path('graph/', viewGraph, name='viewGraph'),
    path('market/', viewMarket, name='viewMarket'),
    path('search/results/', doSearch),
    path('about/', aboutPageView),
    path('accounts/', include('allauth.urls')),
    path('question/<int:id>/', questionView),
    path('question/<int:id>/vote', questionVoteView),
    path('answer/<int:id>/vote', answerVoteView),
    path('question/<int:id>/answer', answerView),
    path('answer/<int:id>/addComment', addComment),
    path('answer/<int:id>/viewAnswer/', viewAnswer),
    path('comment/<int:id>/saveComment/', saveComment),
    path('comment/<int:id>/', viewComment),
    path('comment/<int:id>/viewUpdateComment/', viewUpdateComment),
    path('comment/<int:id>/updateComment/', updateComment),
    path('answer/<int:id>/update', updateAnswer),
    path('answer/<int:id>/saveAnswer/', saveAnswer),
    path('question/new/', newView),
    path('question/<int:id>/update/', update),
    #path('question/<int:id>/update/', updateQuestionView),
    path('question/<int:id>/updateQuestion/', updateQuestion),
    #path('question/updateQuestion/', updateQuestion),
    path('question/my_answers/', myAnswersView, name='my-answers'),
    path('question/my_comments/', myCommentsView, name='my-comments'),
    path('question/my_questions/', myQuestionsView, name='my-questions'),
    path('question/my_words/', myWordsView, name='my-words'),
    path('transactions/my_transactions/', myTransactionsView, name='my-transactions'),
]
