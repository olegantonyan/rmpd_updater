# -*- coding: utf-8 -*-

import logging
import os
import shutil
import importlib.machinery

import shell

log = logging.getLogger(__name__)


class Archive(object):
    def __init__(self, use_sudo=False):
        self._sudo = use_sudo

    def compress(self, source_path, destination_filepath):
        log.debug('compressing "%s" to "%s"', source_path, destination_filepath)
        (r, o, e) = shell.execute(self._sudo_prefix() + 'tar -czvf {dst} -C {src} .'.format(dst=destination_filepath, src=source_path))
        if r != 0:
            log.error('error compressing "%s" to "%s"\n%s', source_path, destination_filepath, e)
            return False
        return True

    def extract(self, source_filepath, destination_path):
        log.debug('extracting "%s" to "%s"', source_filepath, destination_path)
        (r, o, e) = shell.execute(self._sudo_prefix() + 'tar -xvf {src} -C {dst}'.format(dst=destination_path, src=source_filepath))
        if r != 0:
            log.error('error extracting "%s" to "%s"\n%s', source_filepath, destination_path, e)
            return False
        return True

    def _sudo_prefix(self):
        if self._sudo:
            return 'sudo '
        else:
            return ''





