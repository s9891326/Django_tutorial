from django.db.models import F
from django.shortcuts import render
from django.utils import timezone

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

# 快捷函数： render() 就不需要loader
from django.shortcuts import render, get_object_or_404

# from django.views.generic import TemplateView

from .models import Question, Choice

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#
#     # return HttpResponse("Hello, world. You're at the polls index.")
#
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#
#     # template = loader.get_template("polls/index.html")
#     # context = {
#     #     "latest_question_list": latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))
#
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # return Question.objects.all()

        # """Return the last five published questions."""
        # return Question.objects.order_by("-pub_date")[:5]

        """
        Return the last five published question (not including those set to be published in the future)
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     return Question.objects.order_by("-pub_date")[:5]


# class IndexView(TemplateView):
#     template_name = "page/index.html"

# def detail(request, question_id):
#     # return HttpResponse("You're looking at question %s." % question_id)
#
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     #     print(question)
#     #     print(question.pub_date)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {"question": question})
#
#     question = get_object_or_404(Question, pk=question_id)
#     print(question)
#     return render(request, 'polls/detail.html', {'question': question})

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# def results(request, question_id):
# #     # response = "You're looking at the results of question %s."
# #     # return HttpResponse(response % question_id)
# #
# #     question = get_object_or_404(Question, pk=question_id)
# #     return render(request, 'polls/results.html', {'question': question})

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)

    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        # selected_choice.votes += 1

        # 使用 F() 避免競爭條件，當多線程時避免第一個線程更新遺失，會根據DB當前的數值進行更新
        # https://docs.djangoproject.com/zh-hans/3.1/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.votes = F('votes') + 1

        selected_choice.save()
        print("vote")

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # 这个函数避免了我们在视图函数中硬编码 URL。它需要我们给出我们想要跳转的视图的名字和该视图所对应的 URL 模式中需要给该视图提供的参数
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
