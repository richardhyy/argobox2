import os
from pathlib import PurePath

os.environ['DJANGO_SETTINGS_MODULE'] = 'argobox.settings'

if __name__ == "__main__":
    print("Preparing django...")
    import django
    django.setup()
    from django.conf import settings
    from api.models import DatasetHistory

    import profile_downloader
    import profile_importer

    FtpConfiguration = {
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


    print("Fetching profile updates...")
    profile_downloader.fetch_profile(FtpConfiguration)

    pending_import = DatasetHistory.objects.filter(imported=False)
    count = pending_import.count()
    print("{} update(s) pending importing.".format(count))

    if count != 0:
        print("Importing updates...")
        for item in pending_import:
            file_path = PurePath(FtpConfiguration['cache_dir']) / item.dataset_type / item.local_filename
            print("Importing {}...".format(file_path))
            try:
                profile_importer.archive_to_database(item.dataset_type, file_path)
                # Mark as imported
                item.imported = True
                item.save()
                os.remove(file_path)
            except Exception as ex:
                print(ex)
                print("Error occurred when importing {}".format(file_path))
    else:
        print("Nothing to import.")

    print("Task complete.")

