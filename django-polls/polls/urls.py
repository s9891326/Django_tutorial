from django.urls import path

from . import views

# 為url名稱添加命名空間
app_name = "polls"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.IndexView.as_view(), name="index"),

    # ex: /polls/5/
    # path('specifics/<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),

    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    path('<int:pk>/results', views.ResultView.as_view(), name='results'),

    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

]

# app_name = 'home'
# # urlpatterns = [
# #     path("", views.IndexView.as_view(), name="index"),
# # ]
