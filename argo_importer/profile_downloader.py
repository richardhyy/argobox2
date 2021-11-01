import ftplib
import uuid
import os
from pathlib import PurePath
from django.utils import timezone

from api.models import DatasetHistory


def fetch_profile(ftp_configuration):
    def retrieve_file(filename, destination):
        print("Downloading {} > {}".format(filename, dest))
        try:
            ftp.retrbinary("RETR " + filename, open(destination, 'wb+').write)
            print("Downloaded {}".format(filename))
            return True
        except Exception as ex:
            print(ex)
            print("Error retrieving remote file: " + filename)
            return False

    if ftp_configuration is None:
        raise Exception("Parameter ftp_configuration is required")

    ftp = ftplib.FTP(ftp_configuration['host'])
    ftp.login(ftp_configuration['user'], ftp_configuration['password'])

    update_interval_hour_given_specified_filename = ftp_configuration['update_interval_hour_given_specified_filename']
    cache_dir = PurePath(ftp_configuration['cache_dir'])
    for dataset_entry in ftp_configuration['remote_datasets']:
        remote_dir = dataset_entry['remote_dir']
        current_dataset_type = dataset_entry['type']

        try:
            ftp.cwd(remote_dir)
        except Exception as ex:
            print(ex)
            print("Skipping fetching {}".format(current_dataset_type))
            continue

        local_data_queryset = DatasetHistory.objects.filter(dataset_type=current_dataset_type)

        dest_dir = cache_dir / current_dataset_type
        os.makedirs(dest_dir, exist_ok=True)

        if 'remote_filename' in dataset_entry.keys():
            remote_filename = dataset_entry['remote_filename']
            existing_history = local_data_queryset.filter(remote_dir=remote_dir, remote_filename=remote_filename).first()

            # Check the need for updating
            if existing_history is not None:
                if not existing_history.need_update(update_interval_hour_given_specified_filename):
                    print("Skipped updating {} profile (last update: {})"
                          .format(current_dataset_type, existing_history.last_update))
                    continue

            unique_local_filename = str(uuid.uuid4())
            dest = dest_dir / unique_local_filename
            if retrieve_file(remote_filename, dest):
                if existing_history is None:
                    DatasetHistory.objects.create(
                        dataset_type=current_dataset_type,
                        remote_dir=remote_dir,
                        remote_filename=remote_filename,
                        local_filename=unique_local_filename,
                        last_update=timezone.now()
                    )
                else:
                    existing_history.last_update = timezone.now()
                    existing_history.imported = False
                    existing_history.save()

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
                if retrieve_file(file, dest):
                    DatasetHistory.objects.create(
                        dataset_type=current_dataset_type,
                        remote_dir=remote_dir,
                        remote_filename=file,
                        local_filename=unique_local_filename,
                        last_update=timezone.now()
                    )

    ftp.quit()


if __name__ == '__main__':
    print("Run cron.py")
