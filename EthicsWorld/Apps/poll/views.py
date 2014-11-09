from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from Apps.poll.models import Question, AvaliableAnswers, Answer
from common import helpers
from django.db.models import Count
from itertools import chain

def Index(request):
    pollData = Question.objects.all()
    htmlData = {
        'polls':pollData
    }
    return render(request, "poll/pollindex.html", htmlData)

def IndividualPoll(request):
    try:
        pollData = Question.objects.get(questionHash = request.GET['pollhash'])
        answerData = AvaliableAnswers.objects.filter(avaliableAnswersQuestionHash = request.GET['pollhash'])
        htmlData = {
            'poll':pollData,
            'avaliableanswers':answerData
        }
        return render(request, "poll/individualpoll.html", htmlData)
    except:
        return HttpResponseRedirect(reverse("poll:index"))

def MakePoll(request):
    try:
        questionHash = helpers.GetHash(request.POST['polltext'])
        newQuestion = Question()
        newQuestion.questionText = request.POST['polltext']
        newQuestion.questionHash = questionHash
        newQuestion.save()
        newAnswers = request.POST.getlist('pollanswer')
        for answer in newAnswers:
            newAnswerModel = AvaliableAnswers()
            newAnswerModel.avaliableAnswersHash = helpers.GetHash(answer)
            newAnswerModel.avaliableAnswersText = answer
            newAnswerModel.avaliableAnswersQuestionHash = questionHash
            newAnswerModel.save()
    finally:
        return HttpResponseRedirect(reverse("poll:index"))

def RenderPollStats(request):
    try:
        responses = Answer.objects.filter(answerQuestionHash = request.GET['questionhash']).values('answerChoiceHash').annotate(total = Count('answerChoiceHash')).order_by('answerChoiceHash')
        avaliableAnswers = AvaliableAnswers.objects.filter(avaliableAnswersQuestionHash = request.GET['questionhash']).order_by('avaliableAnswersHash')
        responseCount = len(Answer.objects.filter(answerQuestionHash = request.GET['questionhash']))
        responseData = zip(responses, avaliableAnswers)
        htmlData = {
            'responsesCount':responseCount,
            'responseData':responseData
        }
        return render(request,"poll/pollstats.html", htmlData)
    except:
        return HttpResponseRedirect(reverse("poll:index"))

def GetPollResponse(request):
    try:
        newAnswer = Answer()
        newAnswer.answerIPOfAnswerer = request.META['REMOTE_ADDR']
        newAnswer.answerChoiceHash = request.POST['pollanswer']
        newAnswer.answerQuestionHash = request.POST['questionhash']
        newAnswer.save()
        return HttpResponseRedirect(reverse("poll:pollstats") + "?questionhash=" + request.POST['questionhash'])
    except:
        return HttpResponseRedirect(reverse("poll:index"))
