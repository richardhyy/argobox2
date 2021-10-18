import os

from collections import OrderedDict
import psycopg2
from os.path import isfile
from datetime import datetime

# import traceback

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'argobox.settings'

    import django
    from django.conf import settings

    # from argo import argo_defaults

    # settings.configure(default_settings=argo_defaults, DEBUG=True)
    django.setup()

    from api import models

    field_format_dict = OrderedDict([
        ('platform_number', '%s'),
        ('cycle_number', '%s'),
        ('date_creation', 'TO_TIMESTAMP(%s,\'YYYYMMDDHH24MISS\')'),
        ('project_name', '%s'),
        ('pi_name', '%s'),
        ('instrument_type', '%s'),
        ('sample_direction', '%s'),
        ('data_mode', '%s'),
        ('julian_day', '%s'),
        ('date', 'TO_TIMESTAMP(%s,\'YYYY-MM-DD\')'),
        ('latitude', '%s'),
        ('longitude', '%s')
    ])


def parse_and_append_header_tsv(profile_path, tsv_path):
    field_dict = OrderedDict([
        ('platformnumber', None),
        ('cyclenumber', None),
        ('datecreation', None),
        ('projectname', None),
        ('piname', None),
        ('instrumenttype', None),
        ('sampledirection', None),
        ('datamode', None),
        ('julianday', None),
        ('date', None),
        ('latitude', None),
        ('longitude', None)
    ])

    remove_list = (
        '(A=Ascend; D=Descend)',
        '(R=Real Time; D=Delayed Mode; A=Real Time Adjusted)',
        ' (days since 1950-01-01 00:00:00 UTC)',
    )

    file = open(profile_path, 'r')
    lines = file.readlines()

    for line in lines:
        line = line.replace('\n', '')

        split = line.split(':', 1)
        if len(split) != 2:
            continue

        split[0] = split[0].replace(' ', '').lower()
        if split[0] in field_dict.keys():
            for remove_keyword in remove_list:
                split[1] = split[1].replace(remove_keyword, '')

            field_dict[split[0]] = split[1].strip()

    # print(field_dict)

    header_line = ''
    if not isfile(tsv_path):
        header_line = '\t'.join(field_dict.keys())

    f = open(tsv_path, 'a')
    f.write(header_line + '\n' + ('\t'.join(field_dict.values())))
    f.close()


def header_tsv_to_json(path):
    file = open(path, 'r')
    lines = file.readlines()

    field_index_dict = {}  # K: index; V: field_name_in_table
    entries = []

    count = 0
    for line in lines:
        line = line.replace('\n', '')

        # ignore empty line
        if line == '':
            continue

        split = line.split('\t')

        # parse the header line
        if count == 0:
            print(split)
            for i in range(0, len(split)):
                header = split[i]

                fields = list(field_format_dict.keys())

                # match field
                match = False
                for field in fields:
                    if header.replace('\ufeff', '') == field.replace('_', ''):
                        field_index_dict[i] = field
                        print('{}[{}] <-> {}'.format(header, i, field))
                        match = True
                        break

                if not match:
                    print('`{}` does not match any field'.format(split[i]))

        else:
            # parse data line
            _entry = {}
            # remaining_field_index = list(field_format_dict.keys())
            for i in range(0, len(split)):
                if i not in field_index_dict:
                    continue

                _value = split[i]
                _entry[field_index_dict[i]] = _value

            entries.append(_entry)

        count += 1

    return entries


if __name__ == "__main__":
    path = input("Path to `argoheader.tsv`: ").replace('\'', '')

    entries = header_tsv_to_json(path)

    print("-----------\n{} argo headers loaded\n-----------".format(len(entries)))

    fields = list(field_format_dict.keys())
    fields_str = ''
    values_str = ''
    first = True
    for field in fields:
        fields_str += (', ' if not first else '') + field
        values_str += (', ' if not first else '') + field_format_dict[field]
        first = False

    datetime_format = '%Y%m%d%H%M%S'
    date_format = '%Y-%m-%d'

    for entry in entries:
        # values = []
        # for key in entry.keys():
        #     values.append(entry[key])
        e = models.Header(
            platform_number=entry['platform_number'],
            cycle_number=entry['cycle_number'],
            date_creation=datetime.strptime(entry['date_creation'], datetime_format),
            project_name=entry['project_name'],
            pi_name=entry['pi_name'],
            instrument_type=entry['instrument_type'],
            sample_direction=entry['sample_direction'],
            data_mode=entry['data_mode'],
            julian_day=entry['julian_day'],
            date=datetime.strptime(entry['date'], date_format),
            latitude=entry['latitude'],
            longitude=entry['longitude'],
        )
        e.save()

    print("Done")
