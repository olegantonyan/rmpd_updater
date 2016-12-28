#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import logging
import logging.handlers
import optparse
import signal
import os

import config
import update
import version
import files


def signal_handler(signum, _):
    logging.info("caught signal {s}".format(s=signum))
    logging.warning("terminated")
    sys.exit(0)


def setup_logger():
    logfile = config.Config().logfile()
    files.mkdir(os.path.dirname(logfile))
    root_logger = logging.getLogger()
    rotating_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=2097152, backupCount=5)
    root_logger.setLevel(logging.DEBUG if (config.Config().verbose_logging()) else logging.INFO)
    child_logger = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] %(name)s[%(threadName)s/%(thread)d] |%(levelname)s| %(message)s", "%Y-%m-%d %H:%M:%S")
    child_logger.setFormatter(formatter)
    rotating_handler.setFormatter(formatter)
    root_logger.addHandler(rotating_handler)
    root_logger.addHandler(child_logger)
    logging.info("started (version %s)", version.VERSION)


def bootstrap(configfile):
    config.Config().set_configfile(configfile)
    setup_logger()
    if configfile and os.path.exists(configfile):
        logging.info("using config file: '{c}'".format(c=configfile))
    else:
        logging.info("using default config")
    logging.info("working directory: '{w}'".format(w=os.getcwd()))
    signal.signal(signal.SIGTERM, signal_handler)


def app():
    upd = update.Update()
    while True:
        try:
            upd.check()
        except KeyboardInterrupt:
            return 0
        except SystemExit:
            return 0
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
    bootstrap(opts.configfile)
    sys.exit(app())

if __name__ == '__main__':
    main()
