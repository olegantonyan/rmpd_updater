# -*- coding: utf-8 -*-

import os
import importlib.machinery


class RmpdClient(object):
    def version(self, install_path):
        module = importlib.machinery.SourceFileLoader('module.name', os.path.join(install_path, 'version.py')).load_module()
        return module.VERSION

