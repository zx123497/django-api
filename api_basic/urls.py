
from django.urls import path
from .views import article_list, article_detail, ptt_article_list, ptt_article_detail

urlpatterns = [
    path('article/', article_list),
    path('article/<int:pk>/', article_detail),
    path('ptt/<int:pk>/', ptt_article_detail),
    path('ptt/', ptt_article_list),
]
