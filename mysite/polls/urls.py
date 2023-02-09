from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path("logout/", views.logout_user, name="logout"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('api/', views.IndexAPIView.as_view()),
    path('api/<int:pk>/update/', views.UpdateView.as_view()),
    path('api/add/', views.AddView.as_view()),
    path('api/<int:pk>/delete/', views.DeleteView.as_view()),
]