from django.db import models


class Header(models.Model):
    platformnumber = models.IntegerField(primary_key=True)
    cyclenumber = models.IntegerField()
    sampledirection = models.CharField(max_length=2, blank=True, null=True)
    datamode = models.CharField(max_length=2, blank=True, null=True)
    julianday = models.CharField(max_length=12, blank=True, null=True)
    datadate = models.CharField(max_length=14, blank=True, null=True)
    qc4date = models.CharField(max_length=1, blank=True, null=True)
    latitude = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    qc4location = models.CharField(max_length=1, blank=True, null=True)
    creationdate = models.CharField(max_length=14, blank=True, null=True)
    updatedate = models.CharField(max_length=14, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'argoheader'
