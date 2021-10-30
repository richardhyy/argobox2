from collections import OrderedDict
from os import listdir


def profile_data_to_json(path):
    def remove_space(text):
        return text.replace(' ', '')

    def contain_ignore_space(full, sub):
        return remove_space(sub) in full

    entry = {}

    # spaces will be removed automatically
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
            line = remove_space(line)
            if contain_ignore_space(line, 'PLATFORM NUMBER'):
                split = line.split(':', 1)
                entry['platform_number'] = split[1]
            elif contain_ignore_space(line, 'CYCLE NUMBER'):
                split = line.split(':', 1)
                entry['cycle_number'] = split[1]
            elif contain_ignore_space(line, 'COLUMN'):
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
        entry[field] = list_str

    return entry


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

    entries = []
    for file in files:
        entries.append(profile_data_to_json(path + "/" + file))

    print("{} meta files loaded".format(len(entries)))

    for entry in entries:
        if models.ArgoCore.objects.filter(platform_number=entry['platform_number'],
                                          cycle_number=entry['cycle_number']).exists():
            # pass if the record already exists
            print("{}@{} - already exists".format(entry['platform_number'], entry['cycle_number']))
            continue

        e = models.ArgoCore(
            platform_number=entry['platform_number'],
            cycle_number=entry['cycle_number'],
            pressure=entry['pressure'],
            cpressure=entry['cpressure'],
            qpressure=entry['qpressure'],
            temperature=entry['temperature'],
            ctemperature=entry['ctemperature'],
            qtemperature=entry['qtemperature'],
            salinity=entry['salinity'],
            csalinity=entry['csalinity'],
            qsalinity=entry['qsalinity']
        )
        e.save()

    print("Done")
