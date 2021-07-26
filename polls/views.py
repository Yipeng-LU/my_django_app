from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question
from django.urls import reverse
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
	if request.method=="GET":
		latest_question_list=Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
		context={"latest_question_list":latest_question_list}
		return render(request,'polls/index.html',context)
	else:
		question_text=request.POST["question_text"]
		pub_date=request.POST["pub_date"]
		choice_text1=request.POST["choice_text1"]
		choice_text2=request.POST["choice_text2"]
		new_question=Question.objects.create(question_text=question_text,pub_date=pub_date)
		new_question.choice_set.create(choice_text=choice_text1)
		new_question.choice_set.create(choice_text=choice_text2)
		return HttpResponseRedirect(reverse("polls:index"))

def detail(request,question_id):
	question=get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()),pk=question_id)
	if request.method=="GET":
		context={"question":question}
		return render(request,'polls/detail.html',context)
	elif request.method=="PUT" or (request.method=='POST' and request.POST["_method"]=="PUT"):
		if request.method=="PUT":
			data=json.loads(request.body.decode('utf-8'))
			question_text=data["question_text"]
			pub_date=data["pub_date"]
			choice_text1=data["choice_text1"]
			choice_text2=data["choice_text2"]
		else:
			question_text=request.POST["question_text"]
			pub_date=request.POST["pub_date"]
			choice_text1=request.POST["choice_text1"]
			choice_text2=request.POST["choice_text2"]
		question.question_text=question_text
		question.pub_date=pub_date
		question.save()
		choice1,choice2=question.choice_set.all()
		choice1.choice_text=choice_text1
		choice1.save()
		choice2.choice_text=choice_text2
		choice2.save()
		return HttpResponseRedirect(reverse("polls:detail",args=(question.id,)))

def results(request,question_id):
	question=get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()),pk=question_id)
	context={"question":question}
	return render(request,'polls/results.html',context)

def vote(request,question_id):
	question=get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()),pk=question_id)
	try:
		selected_choice_id=request.POST["choice"]
		selected_choice=question.choice_set.get(pk=selected_choice_id)
	except:
		context={"question":question,"error_msg":"You didn't select a choice"}
		return render(request,'polls/detail.html',context)
	else:
		selected_choice.votes+=1
		selected_choice.save()
		return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))

def new(request):
	return render(request,'polls/new.html')

def edit(request,question_id):
	question=get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()),pk=question_id)
	choices=question.choice_set.all()
	context={"question":question,"choices":choices}
	return render(request,'polls/edit.html',context)

def delete(request,question_id):
	if request.method=="DELETE" or (request.method=="POST" and request.POST["_method"]=="DELETE"):
		question=get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()),pk=question_id)
		question.delete()
		return HttpResponseRedirect(reverse("polls:index"))