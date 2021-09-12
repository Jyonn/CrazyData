from SmartDjango import Analyse
from django.views import View

from Base.auth import Auth
from Project.models import ProjectP, Project


class BaseView(View):
    @staticmethod
    @Analyse.r([ProjectP.name])
    @Auth.require_login
    def post(r):
        project = Project.new(r.d.name, r.user)
        return project.d_owner()

    @staticmethod
    @Auth.require_login
    def get(r):
        return Project.objects.filter(owner=r.user).dict(Project.d)


class IDView(View):
    @staticmethod
    @Analyse.r(a=[ProjectP.project])
    def get(r):
        return r.d.project.d()

    @staticmethod
    @Analyse.r(a=[ProjectP.project])
    def delete(r):
        r.d.project.remove()
        return 0


class TicketView(View):
    @staticmethod
    @Analyse.r(a=[ProjectP.project])
    @Auth.require_login
    def get(r):
        return r.d.project.ticket

    @staticmethod
    @Analyse.r(a=[ProjectP.project])
    @Auth.require_login
    def post(r):
        r.d.project.refresh_ticket()
        return r.d.project.ticket
