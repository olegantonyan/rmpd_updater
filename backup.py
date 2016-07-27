# -*- coding: utf-8 -*-

import logging
import os

import config
import archive
import rmpd_client

log = logging.getLogger(__name__)


class Backup(object):
    def __init__(self):
        self._install_path = config.Config().rmpd_client_path()

    def run(self):
        backup_filename = '{prefix}{version}.tar.gz'.format(prefix=self._backup_file_prefix(), version=self._read_version())
        destination_filepath = self._final_destination(backup_filename)
        log.info('starting backup "%s" to "%s"', self._install_path, destination_filepath)
        if not archive.Archive().compress(self._install_path, destination_filepath):
            log.error('error running backup')
            return False
        log.info('backup successfully finished, the file stored in %s', destination_filepath)
        return True

    def restore(self, file):
        if not archive.Archive(True).extract(file, self._install_path):
            log.error('error restoring backup %s', file)
            return False
        return True

    def restore_most_recent(self):
        file = self.most_recent_backup()
        if file is None:
            log.error('no recent backups found')
            return False
        return self.restore(file)

    def backup_storage_dir(self):
        directory = os.path.join(os.getcwd(), 'backups')
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def most_recent_backup(self):
        files = [f for f in os.listdir(self.backup_storage_dir()) if f.startswith(self._backup_file_prefix())]
        if len(files) == 0:
            return None
        return self._final_destination(max(files, key=lambda f: os.path.getctime(self._final_destination(f))))

    def _backup_file_prefix(self):
        return 'backup-rmpd-client-'

    def _final_destination(self, file):
        return os.path.join(self.backup_storage_dir(), file)

    def _read_version(self):
        return rmpd_client.RmpdClient().version(self._install_path)





