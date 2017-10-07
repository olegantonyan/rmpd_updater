# -*- coding: utf-8 -*-

import logging
import os
import time

import config
import backup
import archive
import shell
import rw_fs

log = logging.getLogger(__name__)


class Update(object):
    def __init__(self):
        self._install_path = config.Config().rmpd_client_path()
        self._backup = backup.Backup()
        self._statefile = 'rmpd_update_statefile'

    def check(self):
        state = self._read_statefile()
        if state == self._processing_state_text():
            return self._wait_processing()
        elif state is not None and os.path.exists(state):
            return self._update(state)
        else:
            log.debug('state in none, nothing to do')
            return None

    def _read_statefile(self):
        try:
            with open(self._statefile, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def _write_statefile(self, data):
        with open(self._statefile, 'w') as f:
            f.write(data)

    def _remove_statefile(self):
        try:
            os.remove(self._statefile)
        except FileNotFoundError:
            pass

    def _update(self, filepath):
        log.info('starting update from %s', filepath)
        with rw_fs.Storage():
            if not os.path.exists(filepath):
                log.error('file %s does not exists', filepath)
                self._remove_statefile()
                return
            with rw_fs.Root():
                if not self._backup.run():
                    log.error('error running backup before update')
                    return
                self._write_statefile(self._processing_state_text())
                try:
                    if not archive.Archive(True).extract(filepath, self._install_path):
                        raise Exception('update extract error')
                    log.info('installing new dependencies')
                    self._install_dependencies()
                except:
                    log.exception('error extracting update, restore most recent backup')
                    if self._backup.restore_most_recent():
                        log.info('recent backup restore successful')
                    else:
                        log.error('error restoring most recent backup')
                    self._write_statefile(self._rollback_state_text())
                log.info('update finished, rebooting')
            self._reboot()

    def _wait_processing(self):
        log.info('update state processing, wait couple minutes')
        time.sleep(180)  # wait a minute or two, after this timeout rollback
        if self._read_statefile() is not None:  # the statefile should be deleted by rmpd_client
            log.info('update state is still processing, something whent wrong, rollback')
            with rw_fs.Root():
                if self._backup.restore_most_recent():
                    self._write_statefile(self._rollback_state_text())
                    try:
                        log.info('restoring old dependencies')
                        self._install_dependencies()
                    except:
                        log.exception('error restoring old dependencies, but cannot do anything with this')
                    self._reboot()
                else:
                    log.error('error restoring most recent backup')
        else:
            log.info('update seems to be successful')

    def _processing_state_text(self):
        return '-PROCESSING-'

    def _rollback_state_text(self):
        return '-ROLLBACK-'

    def _reboot(self):
        shell.execute('sync')
        shell.execute('sudo reboot')
        while True:
            time.sleep(1)

    def _install_dependencies(self):
        (r, o, e) = shell.execute('sudo pip3 install -r {path}/requirements.txt'.format(path=self._install_path))
        if r != 0:
            raise Exception('{e}\n{o}'.format(e=e, o=o))
