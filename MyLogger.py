#!/usr/bin/env python

# Author - Shane Carnahan
# Email  - Shane.Carnahan1@gmail.com
# Date - 8/13/2018
# Project - The_Extractor
# Version - 1.0

import os
import logging
import logging.handlers

def my_logger(name=None, log_file_name=None):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        file_logger = logging.handlers.RotatingFileHandler(filename=log_file_name, mode='w', encoding=None, delay=False, maxBytes=1000000000, backupCount=5)
        file_formatter = logging.Formatter('%(asctime)s:%(name)-12s:%(levelname)-8s:%(message)s')
        file_logger.setFormatter(file_formatter)

        # define a Handler which writes INFO messages or higher to the sys.stderr
        console_logger = logging.StreamHandler()
        console_logger.setLevel(logging.INFO)
        # set a format which is simpler for console_logger use
        console_formatter = logging.Formatter('%(name)-12s:%(levelname)-8s:%(message)s')
        # tell the handler to use this format
        console_logger.setFormatter(console_formatter)
        # add the handler to the root logger
        logger.addHandler(console_logger)
        logger.addHandler(file_logger)
        # logging.getLogger('').addHandler(console_logger)
        # logging.getLogger('').addHandler(file_logger)

        return logger
    else:
        return logger

