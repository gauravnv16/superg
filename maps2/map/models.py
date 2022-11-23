from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class Place(models.Model):
    latitude = models.CharField(verbose_name=_(u"Latitude"), max_length=32)
    longitude = models.CharField(verbose_name=_(u"Longitude"), max_length=32)
    address = models.CharField(verbose_name=_(u"Address"), max_length=128)

    class Meta:
        unique_together = ("latitude", "longitude")

    def __unicode__(self):
        return "%s - %s - %s" % (self.latitude, self.longitude, self.address)
