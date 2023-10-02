from typing import Any
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import task
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def login_user(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username , password = password)
        
        if user is not None:
            login(request, user)
            return redirect("tasklist")

        
    return render(request,'base/login.html')

def logout_user(request):
    
    logout(request)
    messages.success(request,"You are Successfully logout")
    return redirect('login')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasklist')
    
    def form_valid(self , form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super(RegisterPage,self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin,ListView):
    model = task
    # This line is for how or with which name object is render basically changing the default name
    context_object_name = 'tasks'
    def get_context_data(self, **kwargs): 
        
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()
        
        search_input = self.request.GET.get('search-area')
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            context['search_input'] = search_input
        
        return context
    
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = task
    context_object_name = 'task'
    # we can also change the template name
    # template_name = 'base/task.html'
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model = task
    fields = ['title','discription','complete']
    success_url = reverse_lazy('tasklist')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = task
    fields = ['title','discription','complete']
    success_url = reverse_lazy('tasklist') 
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = task
    context_object_name = 'task'
    success_url = reverse_lazy("tasklist")