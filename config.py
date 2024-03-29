# -*- coding: utf-8 -*-

import configparser
import codecs
import os

import singleton


class Config(object, metaclass=singleton.Singleton):
    def __init__(self):
        self._filename = None
        self._parser = None

    def set_configfile(self, filename):
        self._filename = filename
        self._parse()

    def rmpd_client_path(self):
        return self._rmpd_client_path

    def logfile(self):
        return self._logfile

    def verbose_logging(self):
        return self._boolean_attr(self._verbose)

    def _boolean_attr(self, attr):
        return attr == 'yes' or attr == 'y' or attr == 'true'

    def _parse(self):
        self._parser = configparser.ConfigParser()
        if self._filename and os.path.exists(self._filename):
            with codecs.open(self._filename, 'r', encoding='utf-8') as f:
                self._parser.read_file(f)

        section = 'logging'
        self._logfile = self._parser.get(section, 'logfile', fallback='/var/log/rmpd/updater.log')
        self._verbose = self._parser.get(section, 'verbose', fallback='no')

        section = 'main'
        self._rmpd_client_path = self._parser.get(section, 'rmpd_client_path', fallback=self._default_rmpd_client_path())

    def _default_rmpd_client_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rmpd_client')


