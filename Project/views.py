from SmartDjango import Analyse
from django.views import View

from Project.models import ProjectP, Project


class BaseView(View):
    @staticmethod
    @Analyse.r([ProjectP.name])
    def post(r):
        project = Project.new(r.d.name)
        return project.d()

    @staticmethod
    def get(_):
        return Project.objects.dict(Project.d)


class IDView(View):
    @staticmethod
    @Analyse.r(a=[ProjectP.project])
    def get(r):
        return r.d.project.d()
