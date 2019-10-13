import datetime

from SmartDjango import models, E, Excp, P
from django.utils.crypto import get_random_string

from Base.common import current_tz, get_time


@E.register
class ProjectError:
    GET_PROJECT = E("获取项目失败")
    PROJECT_NOT_FOUND = E("找不到项目")
    NEW_PROJECT = E("新建项目错误")


class Project(models.Model):
    name = models.CharField(
        verbose_name='项目名称',
        max_length=20,
    )

    pid = models.CharField(
        verbose_name='项目ID',
        max_length=4,
        unique=True,
    )

    create_time = models.DateTimeField(
        verbose_name='创建时间',
        default=0,
    )

    @classmethod
    @Excp.pack
    def get(cls, pid):
        try:
            return cls.objects.get(pid=pid)
        except cls.DoesNotExist:
            return ProjectError.PROJECT_NOT_FOUND
        except Exception:
            return ProjectError.GET_PROJECT

    @classmethod
    def get_unique_pid(cls):
        while True:
            pid = get_random_string(length=4)
            try:
                cls.get(pid)
            except Excp as ret:
                if ret.eis(ProjectError.PROJECT_NOT_FOUND):
                    return pid

    @classmethod
    @Excp.pack
    def new(cls, name):
        crt_time = get_time()
        try:
            project = cls(name=name, pid=cls.get_unique_pid(), create_time=crt_time)
            project.save()
        except Exception:
            return ProjectError.NEW_PROJECT
        return project

    def _readable_create_time(self):
        return self.create_time.timestamp()

    def d(self):
        return self.dictor('name', 'pid', 'create_time')


class ProjectP:
    name, pid = Project.P('name', 'pid')
    project = pid.clone().process(P.Processor(Project.get, yield_name='project'))
