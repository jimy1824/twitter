from django.urls import path, re_path
from tweets import views

urlpatterns = [
    path('users/<str:twitter_user_name>', views.TweetsListView.as_view(), name='tweets_list'),

]
