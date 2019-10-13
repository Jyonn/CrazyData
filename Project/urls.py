from django.urls import path

from Project.views import BaseView, IDView

urlpatterns = [
    path('', BaseView.as_view()),
    path('/@<path:pid>', IDView.as_view()),
]
