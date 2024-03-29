# -*- coding: utf-8 -*-

import os
import importlib.machinery

import shell


class RmpdClient(object):
    def version(self, install_path):
        module = importlib.machinery.SourceFileLoader('module.name', os.path.join(install_path, 'version.py')).load_module()
        return module.VERSION

    def stop(self):
        shell.execute('sudo systemctl stop rmpd')

    def start(self):
        shell.execute('sudo systemctl start rmpd')


