from collections import OrderedDict
from os import listdir
from datetime import datetime
from django.utils import timezone

datetime_format = '%Y%m%d%H%M%S'
date_format = '%Y-%m-%d'


def parse_profile_data(path):
    def remove_space(text):
        return text.replace(' ', '')

    def contain_ignore_space(full, sub):
        return remove_space(sub) in full

    # spaces will be removed automatically
    meta_prefix_field_dict = {
        'PLATFORM NUMBER': 'platform_number',
        'CYCLE NUMBER': 'cycle_number',
        'DATE CREATION': 'date_creation',
        'PROJECT NAME': 'project_name',
        'PI NAME': 'pi_name',
        'INSTRUMENT TYPE': 'instrument_type',
        'SAMPLE DIRECTION': 'sample_direction',
        'DATA MODE': 'data_mode',
        'JULIAN DAY': 'julian_day',
        'DATE': 'date',
        'LATITUDE': 'latitude',
        'LONGITUDE': 'longitude'
    }

    column_header_prefix_field_dict = {
        'Pressure (dbar)': 'pressure',
        'Corrected Pressure (dbar)': 'cpressure',
        'Quality on Pressure': 'qpressure',
        'Temperature (degree_Celsius)': 'temperature',
        'Corrected Temperature (degree_Celsius)': 'ctemperature',
        'Quality on Temperature': 'qtemperature',
        'Salinity (PSU)': 'salinity',
        'Corrected Salinity (PSU)': 'csalinity',
        'Quality on Salinity': 'qsalinity'
    }

    column_index_field_dict = {}

    file = open(path, 'r')
    lines = file.readlines()

    out_entries = {
        'meta': {},
        'data': {}
    }

    data_table = {}

    data_section = False
    for line in lines:
        line = line.replace('\n', '')
        if line == '':
            continue

        if line.startswith('=============='):
            data_section = True

            for index in column_index_field_dict.keys():
                data_table[index] = []

            continue

        if data_section:
            line = line.replace('  ', ' ').replace('  ', ' ')
            line = line.removeprefix(' ').removesuffix(' ')
            split = line.split(' ')
            for i in range(0, len(split)):
                _value = split[i]
                data_table[i].append(_value)
        else:
            original_line = line
            # store the original line text because some data contains space and we don't want to discard them when saving
            line = remove_space(line)
            contains_meta = False
            for key, value in meta_prefix_field_dict.items():
                # if the line contains the meta info we need
                split = original_line.split(':', 1)
                if remove_space(split[0]) == remove_space(key):
                    # Get string on the lhs of '('
                    # Example (We need 'A' here):
                    #     SAMPLE DIRECTION      :A(A=Ascend; D=Descend)
                    if '(' in split[1]:
                        split[1] = split[1].split('(', 1)[0]
                    out_entries['meta'][value] = split[1].replace('"', '\\"')  # escaping double quote
                    contains_meta = True
                    break
            if not contains_meta and contain_ignore_space(line, 'COLUMN'):
                # Example:
                #     COLUMN 1              :Pressure (dbar)                             F7.1
                split = line.split(':', 1)
                _index = int(split[0].removeprefix('COLUMN')) - 1
                _field_name = None
                for prefix in column_header_prefix_field_dict.keys():
                    if split[1].startswith(remove_space(prefix)):
                        _field_name = column_header_prefix_field_dict[prefix]

                if _field_name == None:
                    print('column `{}` does not match with any known fields'.format(split[1]))
                else:
                    column_index_field_dict[_index] = _field_name

    for col_index in column_index_field_dict.keys():
        field = column_index_field_dict[col_index]
        list_str = '{' + (','.join(data_table[col_index])) + '}'
        out_entries['data'][field] = list_str

    return out_entries


if __name__ == "__main__":
    import os

    os.environ['DJANGO_SETTINGS_MODULE'] = 'argobox.settings'

    import django
    from django.conf import settings

    # from argo import argo_defaults

    # settings.configure(default_settings=argo_defaults, DEBUG=True)
    django.setup()

    from api import models

    from os.path import isfile, join

    path = input("Path to Argo core profile folder: ").replace('\'', '')
    files = [f for f in listdir(path) if isfile(join(path, f))]

    print("Parsing data...")

    profile_entries = []
    for file in files:
        profile_entries.append(parse_profile_data(path + "/" + file))

    print("{} profile files loaded".format(len(profile_entries)))

    for entry in profile_entries:
        # Save meta
        meta_entry = entry['meta']
        if models.ArgoHeader.objects.filter(platform_number=meta_entry['platform_number'],
                                            cycle_number=meta_entry['cycle_number']).exists():
            # pass if the record already exists
            print("Header {}@{} - already exists".format[meta_entry['platform_number'], meta_entry['cycle_number']])
            continue

        try:
            e = models.ArgoHeader(
                platform_number=meta_entry['platform_number'],
                cycle_number=meta_entry['cycle_number'],
                date_creation=datetime.strptime(meta_entry['date_creation'], datetime_format),
                project_name=meta_entry['project_name'],
                pi_name=meta_entry['pi_name'],
                instrument_type=meta_entry['instrument_type'],
                sample_direction=meta_entry['sample_direction'],
                data_mode=meta_entry['data_mode'],
                julian_day=meta_entry['julian_day'],
                date=datetime.strptime(meta_entry['date'], date_format),
                latitude=meta_entry['latitude'],
                longitude=meta_entry['longitude'],
            )
            e.save()
        except Exception as ex:
            raise ex

        # Save profile data
        data_entry = entry['data']
        if models.ArgoCore.objects.filter(platform_number=meta_entry['platform_number'],
                                          cycle_number=meta_entry['cycle_number']).exists():
            # pass if the record already exists
            print("Core profile {}@{} - already exists".format(meta_entry['platform_number'], meta_entry['cycle_number']))
            continue

        try:
            e = models.ArgoCore(
                platform_number=meta_entry['platform_number'],
                cycle_number=meta_entry['cycle_number'],
                pressure=data_entry['pressure'],
                cpressure=data_entry['cpressure'],
                qpressure=data_entry['qpressure'],
                temperature=data_entry['temperature'],
                ctemperature=data_entry['ctemperature'],
                qtemperature=data_entry['qtemperature'],
                salinity=data_entry['salinity'],
                csalinity=data_entry['csalinity'],
                qsalinity=data_entry['qsalinity']
            )
            e.save()
        except Exception as ex:
            raise ex

    print("Done")
