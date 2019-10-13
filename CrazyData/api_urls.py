from django.urls import path, include

urlpatterns = [
    path('/project', include('Project.urls')),
    path('/segment', include('Segment.urls')),
]
