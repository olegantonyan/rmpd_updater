# -*- coding: utf-8 -*-

import os
import getpass

import shell


def mkdir(path):
    shell.execute("sudo mkdir -p {p}".format(p=path))
    chown_to_current(path)


def chmod(path, mode):
    shell.execute("sudo chmod -R {m} {p}".format(p=path, m=mode))


def chown(path, user, group):
    shell.execute("sudo chown -R {u}:{g} {p}".format(p=path, u=user, g=group))


def chown_to_current(path):
    chown(path, getpass.getuser(), os.getegid())


