# -*- coding: utf-8 -*-

import logging
import os
import shutil
import importlib.machinery

import config
import archive

log = logging.getLogger(__name__)


class Backup(object):
    def __init__(self):
        self._install_path = config.Config().rmpd_client_path()

    def run(self):
        backup_filename = '{prefix}{version}.tar.gz'.format(prefix=self._backup_file_prefix(), version=self._read_version())
        temp_destination_filepath = os.path.join('/tmp', backup_filename)
        log.info('starting backup "%s" to "%s"', self._install_path, temp_destination_filepath)
        if not archive.Archive().compress(self._install_path, temp_destination_filepath):
            log.error('error running backup')
            return False
        final_destination = self._final_destination(backup_filename)
        try:
            shutil.move(temp_destination_filepath, final_destination)
        except:
            log.exception('error moving backup file after successful backup')
            return False
        log.info('backup successfully finished, the file stored in %s', final_destination)
        return True

    def restore(self, file):
        pass

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
        module = importlib.machinery.SourceFileLoader('module.name', os.path.join(self._install_path, 'version.py')).load_module()
        return module.VERSION





