# -*- coding: utf-8 -*-

import re
import os
import time
import logging


class UTCFormatter(logging.Formatter):

    log_suffix = None
    converter = time.gmtime

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%dT%H:%M:%S", ct)
            s = "%s.%03dZ" % (t, record.msecs)
        return s

    def __get_log_suffix(self):
        if self.log_suffix is None:
            self.log_suffix = os.environ.get('METWORK_LOG_SUFFIX', False)
        if self.log_suffix is False:
            return None
        return self.log_suffix

    def format(self, record):
        strg = logging.Formatter.format(self, record)
        suffix = self.__get_log_suffix()
        if suffix is None:
            return strg
        else:
            return "%s %s" % (strg, suffix)


class OneLineSafeUTCFormatter(UTCFormatter):

    forbidden_characters = "[^a-zA-Z0-9\_\-\.\:\,]"

    def format(self, record):
        record.message = re.sub(self.forbidden_characters, ' ',
                                record.message)
        return UTCFormatter.format(self, record)
