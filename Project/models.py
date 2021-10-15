from SmartDjango import models, E
from django.utils.crypto import get_random_string
from smartify import Processor

from Base.common import get_time


@E.register()
class ProjectError:
    GET_PROJECT = E("获取项目失败")
    PROJECT_NOT_FOUND = E("找不到项目")
    NEW_PROJECT = E("新建项目错误")
    TICKET_INVALID = E("项目凭证错误或过期")


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

    owner = models.ForeignKey(
        'User.User',
        on_delete=models.CASCADE,
        default=None,
    )

    ticket = models.CharField(
        verbose_name='项目录入凭证',
        max_length=64,
        default=None,
    )

    visit_num = models.IntegerField(
        verbose_name='访问人数',
        default=0,
    )

    @classmethod
    def get(cls, pid):
        try:
            return cls.objects.get(pid=pid)
        except cls.DoesNotExist:
            raise ProjectError.PROJECT_NOT_FOUND
        except Exception as err:
            raise ProjectError.GET_PROJECT(debug_message=err)

    @classmethod
    def get_unique_pid(cls):
        while True:
            pid = get_random_string(length=4)
            try:
                cls.get(pid)
            except E as e:
                if e.eis(ProjectError.PROJECT_NOT_FOUND):
                    return pid

    @classmethod
    def new(cls, name, owner):
        crt_time = get_time()
        try:
            project = cls(
                name=name,
                pid=cls.get_unique_pid(),
                create_time=crt_time,
                owner=owner,
                ticket=get_random_string(length=64)
            )
            project.save()
        except Exception as err:
            raise ProjectError.NEW_PROJECT(debug_message=err)
        return project

    def _readable_create_time(self):
        return self.create_time.timestamp()

    def _readable_owner(self):
        return self.owner.d()

    def d(self):
        self.visit_num += 1
        self.save()
        return self.dictor('name', 'pid', 'create_time', 'owner')

    def d_owner(self):
        return self.dictor('name', 'pid', 'create_time', 'owner', 'ticket')

    def refresh_ticket(self):
        self.ticket = get_random_string(length=64)
        self.save()

    def auth_ticket(self, ticket):
        return self.ticket == ticket

    def remove(self):
        self.delete()


class ProjectP:
    name, pid, ticket = Project.P('name', 'pid', 'ticket')
    project = pid.clone().process(Processor(Project.get, yield_name='project'))
