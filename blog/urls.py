from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='about'),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('<int:pk>/comment/', views.comment_like, name='comment-like'),
]