from django.shortcuts import render
from main.models import Comment, Question
from users.models import User
from django.core.paginator import Paginator

def homeFeedView(request):
    current_user = request.user
    
    questions = Question.objects.filter(points__gt=-2, hidden=False).order_by('-created')
    comments = Comment.objects.all().order_by('-created')[0:1]
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    questions_exist = len(questions) > 0
    context = {
        'current_user': current_user,
        'page_obj': page_obj,
        'questions_exist': questions_exist,
        'comments':comments
    }
    return render(request, 'home.html', context)

def leaderboardView(request):
    current_user = request.user

    leaders = User.objects.filter(points__gt=0).order_by('-points')[:25]
    context = {'current_user': current_user, 'leaders': leaders}
    return render(request, 'leaderboard.html', context)


from django.shortcuts import render
from django.http import HttpResponse
from bokeh.plotting import figure
from bokeh.embed import components

def testView(request):
    # current_user = request.user
    # context = {'username': current_user.username,
    #            'current_user': current_user}
    # return render(request, 'test.html', context)
    #create a plot
    print('Giao dien')
    plot = figure(plot_width=400, plot_height=400)
 
   # add a circle renderer with a size, color, and alpha
 
    plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
 
    script, div = components(plot) 
    return render(request, 'test.html', {'script': script, 'div': div})
