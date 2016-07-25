# -*- coding: utf-8 -*-

import logging
import os
import shutil
import importlib.machinery
import time

import shell
import config
import backup

log = logging.getLogger(__name__)


class Update(object):
    def __init__(self):
        self._path = config.Config().rmpd_client_path()
        self._backup = backup.Backup()

    def run(self, filename):
        log.info('starting software update from %s', filename)
        if not self._backup.run():
            log.error('software update interrupted due to failed backup')
            return False

    def check(self):
        state = self._read_statefile()
        if state is None:
            return None
        elif state == '-PROCESSING-':
            time.sleep(120)  # wait a minute or two, after this timeout rollback
            if self._read_statefile() is not None:
                self._backup.restore_most_recent()
        else:
            pass  # start update from file named in `state`

    def _read_statefile(self):
        try:
            with open(config.Config().statefile(), 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None








