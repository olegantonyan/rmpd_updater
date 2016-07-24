# -*- coding: utf-8 -*-

import logging
import os
import shutil

import utils.shell as shell
import version

log = logging.getLogger(__name__)


class Update(object):
    def __init__(self):
        self._backup = Backup()

    def run(self):
        log.info('starting software update')
        if not self._backup.run():
            log.error('software update interrupted due to failed backup')
            return False


class Backup(object):
    def __init__(self):
        self._install_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

    def run(self):
        backup_filename = '{prefix}{version}.tar.gz'.format(prefix=self._backup_file_prefix(), version=version.VERSION)
        temp_destionation_file_path = os.path.join('/tmp', backup_filename)
        log.info('starting backup %s to %s', self._install_path, temp_destionation_file_path)
        (r, o, e) = shell.execute('tar -czvf {file} -C {path} .'.format(file=temp_destionation_file_path, path=self._install_path))
        if r != 0:
            log.error('error running backup\n%s', e)
            return False
        final_destination = self._final_destination(backup_filename)
        try:
            shutil.move(temp_destionation_file_path, final_destination)
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





