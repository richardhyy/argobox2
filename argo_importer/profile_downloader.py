import ftplib
import uuid
import os
from pathlib import PurePath
from os import listdir
from os.path import isfile, join
from datetime import datetime
from django.utils import timezone

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'argobox.settings'
    import django

    django.setup()

    from django.conf import settings

from api.models import DatasetHistory

DefaultFtpConfiguration = {
    'host': 'ftp.argo.org.cn',
    'user': None,
    'password': None,
    'update_interval_hour_given_specified_filename': 24,
    'cache_dir': settings.BASE_DIR / 'cache' / 'dataset',
    'remote_datasets': [
        {
            'type': 'core',
            'remote_dir': '/pub/ARGO/global/core',
            'retrieve_limit': 3
        },
        {
            'type': 'bbp',
            'remote_dir': '/pub/ARGO/global/bgc',
            'remote_filename': 'bgc_argo_bbp_prof.tar.gz'
        },
        {
            'type': 'cdom',
            'remote_dir': '/pub/ARGO/global/bgc',
            'remote_filename': 'bgc_argo_cdom_prof.tar.gz'
        },
        {
            'type': 'chla',
            'remote_dir': '/pub/ARGO/global/bgc',
            'remote_filename': 'bgc_argo_chla_prof.tar.gz'
        },
        {
            'type': 'doxy',
            'remote_dir': '/pub/ARGO/global/bgc',
            'remote_filename': 'bgc_argo_doxy_prof.tar.gz'
        },
        {
            'type': 'irra',
            'remote_dir': '/pub/ARGO/global/bgc',
            'remote_filename': 'bgc_argo_irra_prof.tar.gz'
        },
        {
            'type': 'nitr',
            'remote_dir': '/pub/ARGO/global/bgc',
            'remote_filename': 'bgc_argo_nitr_prof.tar.gz'
        },
        {
            'type': 'ph',
            'remote_dir': '/pub/ARGO/global/bgc',
            'remote_filename': 'bgc_argo_ph_prof.tar.gz'
        },
    ]
}


def fetch_profile(ftp_configuration=None):
    def retrieve_file(filename, destination):
        try:
            ftp.retrbinary("RETR " + filename, open(destination, 'wb+').write)
        except Exception as ex:
            print(ex)
            print("Error retrieving remote file: " + filename)

    if ftp_configuration is None:
        ftp_configuration = DefaultFtpConfiguration
    ftp = ftplib.FTP(ftp_configuration['host'])
    ftp.login(ftp_configuration['user'], ftp_configuration['password'])

    cache_dir = PurePath(ftp_configuration['cache_dir'])
    for dataset_entry in ftp_configuration['remote_datasets']:
        remote_dir = dataset_entry['remote_dir']
        current_dataset_type = dataset_entry['type']

        ftp.cwd(remote_dir)
        local_data_queryset = DatasetHistory.objects.filter(dataset_type=current_dataset_type)

        dest_dir = cache_dir / current_dataset_type
        os.makedirs(dest_dir, exist_ok=True)

        if 'remote_filename' in dataset_entry.keys():
            print('Not implemented')
        else:
            # Detect file changes in folder
            data = []
            ftp.dir(data.append)

            remote_file_list = sorted([line.replace('  ', '').split(' ')[-1] for line in data], reverse=True)
            # Extract latest n files
            if 'retrieve_limit' in dataset_entry.keys() and dataset_entry['retrieve_limit'] > 0:
                limit = dataset_entry['retrieve_limit']
                remote_file_list = remote_file_list[0:min(limit, len(remote_file_list))]

            # Exclude downloaded files
            remote_file_set = set(remote_file_list)
            local_file_set = set([entry['remote_filename'] for entry in local_data_queryset.values()])
            new_files = remote_file_set - local_file_set

            # Download new files in DESC order
            ordered_remote_file = sorted(list(new_files))

            print("{} file(s) pending for {}".format(len(ordered_remote_file), current_dataset_type))
            for file in ordered_remote_file:
                unique_local_filename = str(uuid.uuid4())
                dest = dest_dir / unique_local_filename
                print("Downloading {} > {}".format(file, dest))
                retrieve_file(file, dest)
                print("Downloaded {}".format(file))
                DatasetHistory.objects.create(
                    dataset_type=current_dataset_type,
                    remote_dir=remote_dir,
                    remote_filename=file,
                    local_filename=unique_local_filename,
                    last_update=timezone.now()
                )

    ftp.quit()


if __name__ == '__main__':
    fetch_profile()
