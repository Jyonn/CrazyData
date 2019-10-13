from SmartDjango import models, E, Excp, P

from Base.common import get_time


@E.register
class SegmentError:
    NEW_SEGMENT = E("新增数据段失败")
    SEGMENT_NOT_FOUND = E("找不到数据段")
    GET_SEGMENT = E("获取数据段失败")

    NEW_WAVE = E("新增数据失败")


class Segment(models.Model):
    project = models.ForeignKey(
        'Project.Project',
        on_delete=models.CASCADE,
    )

    time = models.DateTimeField(
        verbose_name='数据产生时间',
        default=0,
        db_index=True,
    )

    @classmethod
    @Excp.pack
    def get(cls, sid):
        try:
            return cls.objects.get(pk=sid)
        except cls.DoesNotExist:
            return SegmentError.SEGMENT_NOT_FOUND
        except Exception:
            return SegmentError.GET_SEGMENT

    @classmethod
    @Excp.pack
    def new(cls, project, time):
        try:
            segment = cls(project=project, time=time)
            segment.save()
        except Exception:
            return SegmentError.NEW_SEGMENT
        return segment

    def _readable_sid(self):
        return self.pk

    def _readable_time(self):
        return self.time.timestamp()

    def _readable_waves(self):
        return Wave.objects.filter(segment=self).dict(Wave.d)

    def d(self):
        return self.dictor('sid', 'time', 'waves')


class SegmentP:
    segment = P('sid', '数据段ID').process(Segment.get)

    time = Segment.get_param('time')
    time = time.clone().set_default(through_processor=True).process(get_time, begin=True)
    time_for_search = time.clone().set_default(0, through_processor=True)


class Wave(models.Model):
    """数据食堂"""
    segment = models.ForeignKey(
        'Segment.Segment',
        on_delete=models.CASCADE,
        db_index=True,
    )

    label = models.CharField(
        verbose_name='数据标签',
        max_length=20,
        null=False,
    )

    value = models.IntegerField(
        verbose_name='数据值',
        max_value=2147483647,
    )

    @classmethod
    @Excp.pack
    def new(cls, segment, label, value):
        try:
            wave = cls(segment=segment, label=label, value=value)
            wave.save()
        except Exception:
            return SegmentError.NEW_WAVE
        return wave

    def d(self):
        return self.dictor('label', 'value')


class WaveP:
    label, value = Wave.P('label', 'value')
