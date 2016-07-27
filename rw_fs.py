# -*- coding: utf-8 -*-

import logging

import shell


log = logging.getLogger(__name__)


class RwFs(object):
    def __enter__(self):
        return self._remount_rootfs(True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._remount_rootfs(False)

    def _is_rootfs_readonly(self):
        (r, o, e) = shell.execute_shell('mount | grep "on / type ext4 (ro,"')
        return len(o) > 0

    def _remount_rootfs(self, rw=True):
        log.debug('remount rootfs')
        if not rw and self._is_rootfs_readonly():
            log.debug('rootfs is already read-only')
            return True
        if rw and not self._is_rootfs_readonly():
            log.debug('rootfs is already read-write')
            return True
        (r, o, e) = shell.execute("sudo mount -o remount,{mode} /".format(mode=('rw' if rw else 'ro')))
        if r != 0:
            log.error('fs remount failed: {e}\n{o}'.format(e=e, o=o))
        return r == 0
