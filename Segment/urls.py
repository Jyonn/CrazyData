from django.urls import path

from Segment.views import BaseView

urlpatterns = [
    path('', BaseView.as_view()),
]
