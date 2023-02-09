from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.views import generic
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from .forms import RegisterUserForm
from django.contrib.auth import logout, login
from .serializers import *
from django.views.generic import *
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.views import *
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import *
from django.contrib.auth.decorators import login_required

class AddView(LoginRequiredMixin,APIView):
    login_url = '/polls/login/'
    def post(self, request):
        permission_classes = (IsAdminUser, )
        serializers = QuestionSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

class UpdateView(LoginRequiredMixin,APIView):
    login_url = '/polls/login/'
    def put(self, request,*args, **kwargs):
        permission_classes = (IsAdminUser,)
        pk = self.kwargs.get("pk", None)
        if not pk:
            return Response({"error":"Method not allowed"})
        try:
            instance = Question.objects.get(pk=pk)
        except:
            return Response({"error": "Method not exist"})
        else:
            serializers = QuestionSerializer(data=request.data, instance=instance)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)

@login_required(login_url='registration/login.html')
class LoginView(LoginRequiredMixin, LoginView):
    template_name = 'registration/login.html'
    redirect_field_name = '/polls/'

    # def form_valid(self, form):
    #     login(self.request, form.get_user())
    #     self.request.session['session_id'] = self.request.user.id
    #     return HttpResponseRedirect(self.get_success_url())


def logout_user(request):
    logout(request)
    return redirect('/polls/login')

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = RegisterUserForm
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/polls')

class DeleteView(LoginRequiredMixin,APIView):
    login_url = '/polls/login/'
    def delete(self, request, *args,**kwargs):
        permission_classes = (IsAdminUser,)
        pk = self.kwargs.get("pk", None)
        if not pk:
            return Response({"error":"Method not allowed"})
        try:
            instance = Question.objects.get(pk=pk)
        except:
            return Response({"error": "Method not exist"})
        else:
            serializers = QuestionSerializer(instance)
            instance.delete()
            return Response(serializers.data)

class IndexAPIView(LoginRequiredMixin,APIView, LimitOffsetPagination):
    login_url = '/polls/login/'
    def get(self, request):
        permission_classes = (IsAuthenticated,)
        q = Question.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 3
        paginator.page_query_param = 'page_size'
        paginator.max_page_size = 100
        result = paginator.paginate_queryset(q, request)
        serializer = QuestionSerializer(result, many=True)
        return Response(serializer.data)

class IndexView(LoginRequiredMixin,generic.ListView):
    login_url = '/polls/login/'
    permission_classes = (IsAuthenticated,)
    template_name = 'polls/index.html'
    context_object_name = "question_list"
    paginate_by = 2

    def get_queryset(self):
        qs = Question.objects.all().distinct()
        qc = UserChoices.objects.filter(user = self.request.user.id).first()
        if not qc:
            return qs
        else:
            for i in qs:
                if i.id in set([j.id for j in self.request.param]):
                    qs = qs.exclude(id=i.id)
            return qs

class DetailView(LoginRequiredMixin,generic.DetailView):
    login_url = '/polls/login/'
    permission_classes = (IsAuthenticated,)
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(LoginRequiredMixin,generic.DetailView):
    login_url = '/polls/login/'
    permission_classes = (IsAuthenticated,)
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        user = User.objects.filter(username = request.user.username).first()
        question = Question.objects.filter(id = question_id).first()
        answer_save = UserChoices(question = question, user =  user)
        answer_save.save()
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))