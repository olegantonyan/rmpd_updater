#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import logging
import optparse
import traceback
import signal
import os

import config


def signal_handler(signum, frame):
    logging.info("caught signal {s}".format(s=signum))
    logging.warning("terminated")
    sys.exit(0)


def setup_logger():
    logging.basicConfig(filename=config.Config().logfile(),
                        format="[%(asctime)s] %(name)s |%(levelname)s| %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=(logging.DEBUG if config.Config().verbose_logging() else logging.INFO))

    root_logger = logging.getLogger()
    child_logger = logging.StreamHandler(sys.stdout)
    child_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] %(name)s |%(levelname)s| %(message)s", "%Y-%m-%d %H:%M:%S")
    child_logger.setFormatter(formatter)
    root_logger.addHandler(child_logger)
    logging.info("started")


def bootstrap(configfile):
    config.Config().set_configfile(configfile)
    setup_logger()
    logging.info("using config file: '{c}'".format(c=configfile))
    logging.info("working directory: '{w}'".format(w=os.getcwd()))
    signal.signal(signal.SIGTERM, signal_handler)


def app():
    while True:
        try:
            pass
        except:
            logging.exception('unhandled exception in main thread')
        time.sleep(21)


def main():
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config-file", dest="configfile", help="path to configration file")
    parser.add_option("-w", "--working-dir", dest="workingdir", help="working directory")

    (opts, args) = parser.parse_args()

    if opts.workingdir:
        os.chdir(opts.workingdir)
    bootstrap(opts.configfile if opts.configfile else "updater.conf")
    sys.exit(app())

if __name__ == '__main__':
    main()
