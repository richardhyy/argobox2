from django.db import models


# class ArgoBoxInformation(models.Model):
#     argo_data_last_update = models.DateTimeField()


class ArgoBbp(models.Model):
    platform_number = models.IntegerField(primary_key=True)
    cycle_number = models.IntegerField()
    pressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    cpressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    qpressure = models.CharField(max_length=1, blank=True, null=True)
    backunknown = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    cbackunknown = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    qbackunknown = models.CharField(max_length=1, blank=True, null=True)
    back470 = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    cback470 = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    qback470 = models.CharField(max_length=1, blank=True, null=True)
    back532 = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    cback532 = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    qback532 = models.CharField(max_length=1, blank=True, null=True)
    back700 = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    cback700 = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    qback700 = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'argobbp'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoCdom(models.Model):
    platform_number = models.IntegerField(primary_key=True)
    cycle_number = models.IntegerField()
    pressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    cpressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    qpressure = models.CharField(max_length=1, blank=True, null=True)
    cdom = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    ccdom = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    qcdom = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'argocdom'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoChla(models.Model):
    platform_number = models.IntegerField(primary_key=True)
    cycle_number = models.IntegerField()
    pressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    cpressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    qpressure = models.CharField(max_length=1, blank=True, null=True)
    chla = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    cchla = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    qchla = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'argochla'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoCore(models.Model):
    platform_number = models.IntegerField()
    cycle_number = models.IntegerField(primary_key=True)
    pressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    cpressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    qpressure = models.CharField(max_length=1, blank=True, null=True)
    temperature = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    ctemperature = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    qtemperature = models.CharField(max_length=1, blank=True, null=True)
    salinity = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    csalinity = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    qsalinity = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'argocore'
        unique_together = (('cycle_number', 'platform_number'),)


class ArgoDoxy(models.Model):
    platform_number = models.IntegerField(primary_key=True)
    cycle_number = models.IntegerField()
    pressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    cpressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    qpressure = models.CharField(max_length=1, blank=True, null=True)
    tempdoxy = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    ctempdoxy = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    qtempdoxy = models.CharField(max_length=1, blank=True, null=True)
    doxygen = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    cdoxygen = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    qdoxygen = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'argodoxy'
        unique_together = (('platform_number', 'cycle_number'),)


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
        managed = False
        db_table = 'argofloat'


class ArgoHeader(models.Model):
    platform_number = models.IntegerField(primary_key=True)
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
        managed = False
        db_table = 'argoheader'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoIrra(models.Model):
    platform_number = models.IntegerField(primary_key=True)
    cycle_number = models.IntegerField()
    pressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    cpressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    qpressure = models.CharField(max_length=1, blank=True, null=True)
    downirra412 = models.DecimalField(db_column='downIrra412', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    cdownirra412 = models.DecimalField(db_column='cdownIrra412', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    qdownirra412 = models.CharField(db_column='qdownIrra412', max_length=1, blank=True, null=True)  # Field name made lowercase.
    downirra443 = models.DecimalField(db_column='downIrra443', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    cdownirra443 = models.DecimalField(db_column='cdownIrra443', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    qdownirra443 = models.CharField(db_column='qdownIrra443', max_length=1, blank=True, null=True)  # Field name made lowercase.
    downirra490 = models.DecimalField(db_column='downIrra490', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    cdownirra490 = models.DecimalField(db_column='cdownIrra490', max_digits=12, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    qdownirra490 = models.CharField(db_column='qdownIrra490', max_length=1, blank=True, null=True)  # Field name made lowercase.
    par = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    cpar = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True)
    qpar = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'argoirra'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoNitr(models.Model):
    platform_number = models.IntegerField(primary_key=True)
    cycle_number = models.IntegerField()
    pressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    cpressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    qpressure = models.CharField(max_length=1, blank=True, null=True)
    nitrate = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    cnitrate = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    qnitrate = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'argonitr'
        unique_together = (('platform_number', 'cycle_number'),)


class ArgoPh(models.Model):
    platform_number = models.IntegerField(primary_key=True)
    cycle_number = models.IntegerField()
    pressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    cpressure = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    qpressure = models.CharField(max_length=1, blank=True, null=True)
    ph = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    cph = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    qph = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'argoph'
        unique_together = (('platform_number', 'cycle_number'),)

# class Header(models.Model):
#     platform_number = models.IntegerField()
#     cycle_number = models.IntegerField()
#     date_creation = models.DateTimeField()
#     project_name = models.CharField(max_length=255)
#     pi_name = models.CharField(max_length=255)
#     instrument_type = models.CharField(max_length=255)
#     sample_direction = models.CharField(max_length=1)
#     data_mode = models.CharField(max_length=1)
#     julian_day = models.FloatField()
#     date = models.DateTimeField()
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#
#     class Meta:
#         db_table = 'argoheader'
