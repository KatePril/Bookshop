from django.urls import path
from .views import *

urlpatterns = [
    path('', BlogIndexView.as_view(), name='blog'),
    path('article/<str:slug>', ArticleDetailView.as_view(), name='article'),
    path('all_articles', AllArticlesView.as_view(), name='all_articles'),
    path('<str:slug>/', ArticleByTag.as_view(), name='tag'),
    path('user_articles/<int:pk>', user_article_list, name='user_articles'),
    path('delete_article/<str:slug>/<int:pk>', delete_article, name='delete_article'),
    path('all_tags', AllTagsView.as_view(), name='all_tags'),
    path('delete_tag/<int:pk>', delete_tag, name='delete_tag')
]
