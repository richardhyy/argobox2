from collections import OrderedDict
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
from django.utils import timezone

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'argobox.settings'
    import django

    django.setup()

from api.models import *

datetime_format = '%Y%m%d%H%M%S'
date_format = '%Y-%m-%d'

ProfileTemplates = {
    'core': {
        'model_name': 'ArgoCore',
        'headers': {
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
    },
    'bbp': {
        'model_name': 'ArgoBbp',
        'headers': {
            'Pressure (dbar)': 'pressure',
            'Corrected Pressure (dbar)': 'cpressure',
            'Quality on Pressure': 'qpressure',
            'Backscattering (m^-1)': 'backunknown',
            'Corrected Backscattering (m^-1)': 'cbackunknown',
            'Quality on Backscattering': 'qbackunknown',
            'Backscattering470 (m^-1)': 'back470',
            'Corrected Backscattering470 (m^-1)': 'cback470',
            'Quality on Backscattering470': 'qback470',
            'Backscattering532 (m^-1)': 'back532',
            'Corrected Backscattering532 (m^-1)': 'cback532',
            'Quality on Backscattering532': 'qback532',
            'Backscattering700 (m^-1)': 'back700',
            'Corrected Backscattering700 (m^-1)': 'cback700',
            'Quality on Backscattering700': 'qback700'
        }
    },
    'cdom': {
        'model_name': 'ArgoCdom',
        'headers': {
            'Pressure (dbar)': 'pressure',
            'Corrected Pressure (dbar)': 'cpressure',
            'Quality on Pressure': 'qpressure',
            'CDOM (ppb)': 'cdom',
            'Corrected CDOM (ppb)': 'ccdom',
            'Quality on CDOM': 'qcdom'
        }
    },
    'chla': {
        'model_name': 'ArgoChla',
        'headers': {
            'Pressure (dbar)': 'pressure',
            'Corrected Pressure (dbar)': 'cpressure',
            'Quality on Pressure': 'qpressure',
            'Chlorophyll-a (mg/m^3)': 'chla',
            'Corrected Chlorophyll-a (mg/m^3)': 'cchla',
            'Quality on Chlorophyll-a': 'qchla'
        }
    },
    'doxy': {
        'model_name': 'ArgoDoxy',
        'headers': {
            'Pressure (dbar)': 'pressure',
            'Corrected Pressure (dbar)': 'cpressure',
            'Quality on Pressure': 'qpressure',
            'TEMP_DOXY (degree_Celsius)': 'tempdoxy',
            'Corrected TEMP_DOXY (degree_Celsius)': 'ctempdoxy',
            'Quality on TEMP_DOXY': 'qtempdoxy',
            'Dissolved Oxygen (micromole/kg)': 'doxygen',
            'Corrected Dissolved Oxygen (micromole/kg)': 'cdoxygen',
            'Quality on dissolved Oxygen': 'qdoxygen',
        }
    },
    'irra': {
        'model_name': 'ArgoIrra',
        'headers': {
            'Pressure (dbar)': 'pressure',
            'Corrected Pressure (dbar)': 'cpressure',
            'Quality on Pressure': 'qpressure',
            'Down Irradiance412 (W/m^2/nm)': 'downirra412',
            'Corrected Down Irradiance412 (W/m^2/nm)': 'cdownirra412',
            'Quality on Down Irradiance412': 'qdownirra412',
            'Down Irradiance443 (W/m^2/nm)': 'downirra443',
            'Corrected Down Irradiance443 (W/m^2/nm)': 'cdownirra443',
            'Quality on Down Irradiance443': 'qdownirra443',
            'Down Irradiance490 (W/m^2/nm)': 'downirra490',
            'Corrected Down Irradiance490 (W/m^2/nm)': 'cdownirra490',
            'Quality on Down Irradiance490': 'qdownirra490',
            'PAR (microMoleQuanta/m^2/sec)': 'par',
            'Corrected PAR (microMoleQuanta/m^2/sec)': 'cpar',
            'Quality on PAR': 'qpar'
        }
    },
    'nitr': {
        'model_name': 'ArgoNitr',
        'headers': {
            'Pressure (dbar)': 'pressure',
            'Corrected Pressure (dbar)': 'cpressure',
            'Quality on Pressure': 'qpressure',
            'Nitrate (micromole/kg)': 'nitrate',
            'Corrected Nitrate (micromole/kg)': 'cnitrate',
            'Quality on Nitrate': 'qnitrate'
        }
    },
    'ph': {
        'model_name': 'ArgoPh',
        'headers': {
            'Pressure (dbar)': 'pressure',
            'Corrected Pressure (dbar)': 'cpressure',
            'Quality on Pressure': 'qpressure',
            'PH in situ total': 'ph',
            'Corrected PH in situ total': 'cph',
            'Quality on PH in situ total': 'qph'
        }
    }
}


def parse_profile_data(path, column_header_prefix_field_dict):
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

                if _field_name is None:
                    print('column `{}` does not match with any known fields'.format(split[1]))
                else:
                    column_index_field_dict[_index] = _field_name

    for col_index in column_index_field_dict.keys():
        field = column_index_field_dict[col_index]
        list_str = '{' + (','.join(data_table[col_index])) + '}'
        out_entries['data'][field] = list_str

    return out_entries


def folder_to_database(profile_type, folder_path):
    if profile_type not in ProfileTemplates.keys():
        raise Exception("No such profile type: {}".format(profile_type))

    template = ProfileTemplates[profile_type]

    files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    print("Parsing data...")

    profile_entries = []
    for file in files:
        profile_entries.append(parse_profile_data(folder_path + "/" + file, template['headers']))

    print("{} profile files loaded".format(len(profile_entries)))
    print("Updating database...")

    meta_affected = 0
    profile_affected = 0

    for entry in profile_entries:
        # Save meta
        meta_entry = entry['meta']
        if ArgoHeader.objects.filter(platform_number=meta_entry['platform_number'],
                                     cycle_number=meta_entry['cycle_number']).exists():
            # pass if the record already exists
            print("Header {}@{} - already exists".format(meta_entry['platform_number'], meta_entry['cycle_number']))
            continue

        try:
            e = ArgoHeader(
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
            meta_affected += 1
        except Exception as ex:
            print("Error inserting metadata for float {}@{}. Profile data insertion skipped".format(meta_entry['platform_number'], meta_entry['cycle_number']))
            print(ex)
            continue

        # Save profile data
        data_entry = entry['data']
        model_class = globals()[
            template['model_name']]  # apps.get_model(app_label='api', model_name=template['model_name'])
        if model_class.objects.filter(platform_number=meta_entry['platform_number'],
                                      cycle_number=meta_entry['cycle_number']).exists():
            # pass if the record already exists
            print(
                "Core profile {}@{} - already exists".format(meta_entry['platform_number'], meta_entry['cycle_number']))
            continue

        try:
            e = model_class()

            setattr(e, 'platform_number', meta_entry['platform_number'])
            setattr(e, 'cycle_number', meta_entry['cycle_number'])

            # fill attributes
            for key, value in data_entry.items():
                setattr(e, key, value)

            e.save()
            profile_affected += 1
        except Exception as ex:
            print("Error inserting profile data for float {}@{}".format(meta_entry['platform_number'], meta_entry['cycle_number']))
            print(ex)

    print("Done. {} ArgoHeader inserted, {} Profile inserted".format(meta_affected, profile_affected))


if __name__ == "__main__":
    profile_type = input("Profile type (avail: {}): ".format(', '.join([name for name in ProfileTemplates.keys()])))
    path = input("Path to Argo {} profile folder: ".format(profile_type)).replace('\'', '')
    folder_to_database(profile_type, path)
