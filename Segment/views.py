from SmartDjango import Analyse, P
from django.views import View

from Base.common import time_dictor, time_pager
from Base.param_limit import PL
from Project.models import ProjectP, ProjectError
from Segment.models import SegmentP, WaveP, Wave, Segment


class BaseView(View):
    @staticmethod
    @Analyse.r({
        ProjectP.project,
        SegmentP.time,
        P('waves').as_list(WaveP.label, WaveP.value),
        ProjectP.ticket,
    })
    def post(r):
        project = r.d.project
        ticket = r.d.ticket
        if not project.auth_ticket(ticket):
            return ProjectError.TICKET_INVALID

        segment = Segment.new(**r.d.dict('project', 'time'))
        for data in r.d.waves:
            Wave.new(segment=segment, **data)

    @staticmethod
    @Analyse.r(q=[
        ProjectP.project,
        SegmentP.time_for_search.clone().rename('last'),
        P('count', '获取数据段个数').process(int).process(PL.number(10, 1)),
    ])
    def get(r):
        project = r.d.project
        last = r.d.last
        count = r.d.count

        page = time_pager.page(Segment.objects.filter(project=project), last=last, count=count)
        return page.dict(object_dictor=Segment.d, next_dictor=time_dictor)
