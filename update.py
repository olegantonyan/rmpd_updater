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
        self._statefile = config.Config().statefile()

    def run(self, filename):
        log.info('starting software update from %s', filename)
        if not self._backup.run():
            log.error('software update interrupted due to failed backup')
            return False

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

    def _update(self, filename):
        with rw_fs.RwFs():
            try:
                log.info('starting update from %s', filename)
                if not self._backup.run():
                    raise Exception('error running backup before update')
                self._write_statefile(self._processing_state_text())
                if not archive.Archive(True).extract(os.path.join(os.getcwd(), filename), self._install_path):
                    raise Exception('update extract error')
                log.info('update finished, rebooting')
                self._reboot()
            except:
                log.exception('error running update')
                log.error('restore most recent backup')
                if self._backup.restore_most_recent():
                    log.info('recent backup restore successful')
                    self._remove_statefile()
                else:
                    log.error('error restoring most recent backup')

    def _wait_processing(self):
        log.info('update state processing, wait couple minutes')
        time.sleep(180)  # wait a minute or two, after this timeout rollback
        if self._read_statefile() is not None:  # the statefile should be deleted by rmpd_client
            log.info('update state is still processing, something whent wrong, rollback')
            if self._backup.restore_most_recent():
                self._remove_statefile()
            else:
                log.error('error restoring most recent backup')
        else:
            log.info('update seems to be successful')

    def _processing_state_text(self):
        return '-PROCESSING-'

    def _reboot(self):
        return shell.execute('sudo reboot')







