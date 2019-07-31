from django.urls import path, re_path
from hashtag import views

urlpatterns = [
    path('hashtags/<str:hashtag>', views.HashTagsListView.as_view(), name='hashtags_list'),

]
