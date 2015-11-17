from django.db import models


class Convention(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return '{name}'.format(name=self.name)


class Event(models.Model):
    convention = models.ForeignKey(Convention, related_name='event_convention_id')
    name = models.CharField(verbose_name='Event Name', max_length=100)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField(verbose_name='Start Time')
    end = models.DateTimeField(verbose_name='End Time')
    size = models.PositiveSmallIntegerField(verbose_name='Max Size', blank=False, null=False)
