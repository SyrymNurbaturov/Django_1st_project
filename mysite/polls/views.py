from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from .models import Question, Choice
from .serializers import *



class IndexAPIView(APIView, LimitOffsetPagination):

    def get(self, request):
        q = Question.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 3
        paginator.page_query_param = 'page_size'
        paginator.max_page_size = 100
        result = paginator.paginate_queryset(q, request)
        serializer = QuestionSerializer(result, many=True)
        return Response(serializer.data)

class AddView(APIView):

    def post(self, request):
        serializers = QuestionSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

class UpdateView(APIView):
    def put(self, request,*args, **kwargs):
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

class DeleteView(APIView):
    def delete(self, request, *args,**kwargs):
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

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))