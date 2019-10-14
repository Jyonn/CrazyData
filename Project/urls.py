from django.urls import path

from Project.views import BaseView, IDView, TicketView

urlpatterns = [
    path('', BaseView.as_view()),
    path('/@<str:pid>', IDView.as_view()),
    path('/@<str:pid>/ticket', TicketView.as_view()),
]
