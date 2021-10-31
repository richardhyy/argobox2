from django.db import models
from django.contrib.postgres.fields import ArrayField


class ArgoFloat(models.Model):
    platform_number = models.IntegerField(primary_key=True)
    transmission_system = models.CharField(max_length=8, blank=True, null=True)
    postioning_system = models.CharField(max_length=16, blank=True, null=True)
    platform_model = models.CharField(max_length=16, blank=True, null=True)
    platform_maker = models.CharField(max_length=24, blank=True, null=True)
    fireware_version = models.CharField(max_length=32, blank=True, null=True)
    serial_number = models.CharField(max_length=8, blank=True, null=True)
    maual_version = models.CharField(max_length=16, blank=True, null=True)
    wmo_type = models.CharField(max_length=3, blank=True, null=True)
    project_name = models.CharField(max_length=64, blank=True, null=True)
    pi_name = models.CharField(max_length=40, blank=True, null=True)
    data_center = models.CharField(max_length=2, blank=True, null=True)
    launch_date = models.CharField(max_length=14, blank=True, null=True)
    launch_latitude = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    launch_longitude = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    launch_platform = models.CharField(max_length=24, blank=True, null=True)
    park_pressure = models.IntegerField(blank=True, null=True)
    profile_pressure = models.IntegerField(blank=True, null=True)
    startup_date = models.CharField(max_length=14, blank=True, null=True)
    cruise_id = models.CharField(max_length=32, blank=True, null=True)
    float_status = models.BooleanField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'argofloat'


class ArgoHeader(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField()
    date_creation = models.DateTimeField()
    project_name = models.CharField(max_length=255)
    pi_name = models.CharField(max_length=255)
    instrument_type = models.CharField(max_length=255)
    sample_direction = models.CharField(max_length=1)
    data_mode = models.CharField(max_length=1)
    julian_day = models.FloatField()
    date = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        managed = True
        db_table = 'argoheader'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoBbp(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField()
    pressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    cpressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    qpressure = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    backunknown = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    cbackunknown = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    qbackunknown = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    back470 = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    cback470 = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    qback470 = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    back532 = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    cback532 = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    qback532 = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    back700 = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    cback700 = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    qback700 = ArrayField(models.CharField(max_length=1, blank=True, null=True))

    class Meta:
        managed = True
        db_table = 'argobbp'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoCdom(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField()
    pressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    cpressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    qpressure = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    cdom = ArrayField(models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True))
    ccdom = ArrayField(models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True))
    qcdom = ArrayField(models.CharField(max_length=1, blank=True, null=True))

    class Meta:
        managed = True
        db_table = 'argocdom'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoChla(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField()
    pressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    cpressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    qpressure = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    chla = ArrayField(models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True))
    cchla = ArrayField(models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True))
    qchla = ArrayField(models.CharField(max_length=1, blank=True, null=True))

    class Meta:
        managed = True
        db_table = 'argochla'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoCore(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField()
    pressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    cpressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    qpressure = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    temperature = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    ctemperature = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    qtemperature = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    salinity = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    csalinity = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    qsalinity = ArrayField(models.CharField(max_length=1, blank=True, null=True))

    class Meta:
        managed = True
        db_table = 'argocore'
        unique_together = (('cycle_number', 'platform_number'),)


class ArgoDoxy(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField()
    pressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    cpressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    qpressure = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    tempdoxy = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    ctempdoxy = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    qtempdoxy = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    doxygen = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    cdoxygen = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    qdoxygen = ArrayField(models.CharField(max_length=1, blank=True, null=True))

    class Meta:
        managed = True
        db_table = 'argodoxy'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoIrra(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField()
    pressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    cpressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    qpressure = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    downirra412 = ArrayField(models.DecimalField(db_column='downIrra412', max_digits=12, decimal_places=6, blank=True, null=True))  # Field name made lowercase.
    cdownirra412 = ArrayField(models.DecimalField(db_column='cdownIrra412', max_digits=12, decimal_places=6, blank=True, null=True))  # Field name made lowercase.
    qdownirra412 = ArrayField(models.CharField(db_column='qdownIrra412', max_length=1, blank=True, null=True))  # Field name made lowercase.
    downirra443 = ArrayField(models.DecimalField(db_column='downIrra443', max_digits=12, decimal_places=6, blank=True, null=True))  # Field name made lowercase.
    cdownirra443 = ArrayField(models.DecimalField(db_column='cdownIrra443', max_digits=12, decimal_places=6, blank=True, null=True))  # Field name made lowercase.
    qdownirra443 = ArrayField(models.CharField(db_column='qdownIrra443', max_length=1, blank=True, null=True))  # Field name made lowercase.
    downirra490 = ArrayField(models.DecimalField(db_column='downIrra490', max_digits=12, decimal_places=6, blank=True, null=True))  # Field name made lowercase.
    cdownirra490 = ArrayField(models.DecimalField(db_column='cdownIrra490', max_digits=12, decimal_places=6, blank=True, null=True))  # Field name made lowercase.
    qdownirra490 = ArrayField(models.CharField(db_column='qdownIrra490', max_length=1, blank=True, null=True))  # Field name made lowercase.
    par = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    cpar = ArrayField(models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True))
    qpar = ArrayField(models.CharField(max_length=1, blank=True, null=True))

    class Meta:
        managed = True
        db_table = 'argoirra'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoNitr(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField()
    pressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    cpressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    qpressure = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    nitrate = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    cnitrate = ArrayField(models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True))
    qnitrate = ArrayField(models.CharField(max_length=1, blank=True, null=True))

    class Meta:
        managed = True
        db_table = 'argonitr'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoPh(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField()
    pressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    cpressure = ArrayField(models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True))
    qpressure = ArrayField(models.CharField(max_length=1, blank=True, null=True))
    ph = ArrayField(models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True))
    cph = ArrayField(models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True))
    qph = ArrayField(models.CharField(max_length=1, blank=True, null=True))

    class Meta:
        managed = True
        db_table = 'argoph'
        unique_together = (('platform_number', 'cycle_number'),)

# class Header(models.Model):
#     platform_number = models.IntegerField()
#     cycle_number = models.IntegerField()
#     date_creation = models.DateTimeField()
#     project_name = ArrayField(models.CharField(max_length=255)
#     pi_name = ArrayField(models.CharField(max_length=255)
#     instrument_type = ArrayField(models.CharField(max_length=255)
#     sample_direction = ArrayField(models.CharField(max_length=1)
#     data_mode = ArrayField(models.CharField(max_length=1)
#     julian_day = models.FloatField()
#     date = models.DateTimeField()
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#
#     class Meta:
#         db_table = 'argoheader'
