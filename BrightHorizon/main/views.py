from django.shortcuts import render
import os
from django.conf import settings
from django import forms
from django.core.files.storage import default_storage
from django.contrib import messages
from django.core.files.base import ContentFile
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from main.forms import SignUpForm, ChPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from main import models
from django.template import loader
from django.template.context_processors import csrf
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.utils.decorators import method_decorator
from django.utils.text import slugify
import uuid
from django.db import connection

from main.models import goal, task, UserGoal, UserTask
from main.forms import AssignGoalForm, RemoveGoalForm, EditTaskForm

# Create your views here.
class PasswordContextMixin:

    extra_context = None

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context.update({

            'title': "Password Update",

            **(self.extra_context or {})

        })

        return context

class PasswordChangeView(PasswordContextMixin, FormView):
   
    form_class = ChPasswordForm
    success_url = reverse_lazy('')
    template_name = 'changepassword.html'
    
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):

        form.save()
        update_session_auth_hash(self.request, form.user)

        return super().form_valid(form)
        
def signup(request):
    if request.user.is_authenticated == True:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = form.cleaned_data.get('email')
            obj.save()

            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render( request, 'index.html')

def assign(request):
    if request.user.is_authenticated == False:
        return redirect('home')

    elif request.method == 'POST':
        if 'assign' in request.POST:
            form = AssignGoalForm(request.POST)
            if form.is_valid():

                obj = form.save(commit=False)
                obj.goal_complete = False
                obj.owner = request.user.username
                tempID = request.POST.get('goalID', None)
                obj.goal_id = tempID
                #obj.goal_id = form.cleaned_data.get('goalid') #< ???
                obj.save()
                

                #Save tasks to user
                goalTasks = task.objects.all().filter(goal_id=tempID)
                for goalTask in goalTasks:
                    userTask = UserTask(task=goalTask, is_completed=False, owner=request.user.username)
                    userTask.save()

                return redirect('assign')
            else:
                return redirect('ThisIsBROKEN.html')

        elif 'remove' in request.POST:
            form = RemoveGoalForm(request.POST)
            if form.is_valid():
                pk = request.POST.get('userGoalID', None)
                post = get_object_or_404(UserGoal, pk=pk)

                #Delete User Tasks
                UserTask.objects.all().filter(owner=request.user.username).filter(task__goal_id=post.goal_id).delete()

                #Delete User Goal
                post.delete()

                return redirect('assign')
            else:
                return redirect('BROKEN.html')

    else:
        assignForm = AssignGoalForm()
        removeForm = RemoveGoalForm()

        goals = goal.objects.all()
        #tasks = Task.objects.all()
        userGoals = UserGoal.objects.all().filter(owner=request.user.username)

        newGoals = []
        for aGoal in goals:
            #if aGoal is not in UserGoals, append.
            goalNotAssigned = True
            for assignedGoal in userGoals:
                if aGoal.id == assignedGoal.goal_id:
                    goalNotAssigned = False
            if goalNotAssigned == True:
                newGoals.append({"id" : aGoal.id, "goal_title" : aGoal.goal_title})

        context = {'goals':newGoals, 'userGoals':userGoals, 'assignForm':assignForm, 'removeForm':removeForm}

        return render( request, 'assign.html', context)

def viewgoals(request):
    if request.user.is_authenticated == False:
        return redirect('home')

    elif request.method == 'POST':
        form = EditTaskForm(request.POST)
        if form.is_valid():
            #Set completed to TRUE
            taskID = request.POST.get('taskID', None)
            aTask = UserTask.objects.get(pk = taskID)
            aTask.is_completed = True
            aTask.save()

            #Check if goal is now completed, if it is, set goal_complete to True.
            goalCompleted = True
            userTasks = UserTask.objects.all().filter(owner=request.user.username).filter(task__goal_id=aTask.task.goal_id)
            for userTask in userTasks:
                if userTask.is_completed == False and userTask.task.is_bonus == False:
                    goalCompleted = False

            if goalCompleted == True:
                aGoals = UserGoal.objects.all().filter(owner=request.user.username).filter(goal_id=aTask.task.goal_id)
                for aGoal in aGoals:
                    aGoal.goal_complete = True
                    aGoal.save()
                    return redirect('viewgoals')

            return redirect('viewgoals')
        else:
            return redirect('ThisIsBROKEN.html')

    else:
        completeForm = EditTaskForm()
        userGoals = UserGoal.objects.all().filter(owner=request.user.username)
        userTasks = UserTask.objects.all().filter(owner=request.user.username)

        totalPoints = 0
        tasksList = []
        for userGoal in userGoals:

            tempTasks = UserTask.objects.all().filter(owner=request.user.username).filter(task__goal_id=userGoal.goal_id)
            if tempTasks:
                tasksList.append(tempTasks)
            else:
                tasksList.append(None)

            if userGoal.goal_complete == True:
                totalPoints = totalPoints + userGoal.goal.points_worth

        #add completed tasks to points
        for userTask in userTasks:
            if userTask.is_completed == True:
                totalPoints = totalPoints + userTask.task.points_worth

        mainList = zip(tasksList, userGoals)
        context = { 'mainList':mainList, 'completeForm':completeForm, 'userGoals':userGoals, 'totalPoints':totalPoints }


        return render( request, 'viewgoals.html', context)