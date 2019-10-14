from django.urls import path

from User.views import OAuthView, BaseView

urlpatterns = [
    path('', BaseView.as_view()),
    path('/oauth', OAuthView.as_view()),
]
