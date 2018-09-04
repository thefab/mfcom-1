# -*- coding: utf-8 -*-

import logging


class AddContextFilter(logging.Filter):
    """Utility class which add some "context" to each log record."""

    def filter(self, record):
        record.extra_space = ''
        if record.levelname == 'DEBUG':
            record.extra_space = '   '
        elif record.levelname == 'INFO':
            record.extra_space = '    '
        elif record.levelname == 'WARNING':
            record.extra_space = ' '
        elif record.levelname == 'ERROR':
            record.extra_space = '   '
        return True


class StdoutFilter(logging.Filter):
    """Filter class which keeps log records for stdout (ie. < WARNING)."""

    def filter(self, record):
        return record.levelno < logging.WARNING


class StderrFilter(logging.Filter):
    """Filter class which keep log records for stderr (ie. >= WARNING)."""

    def filter(self, record):
        return record.levelno >= logging.WARNING


class IgnoreAllFilter(logging.Filter):
    """Filter class which ignore eveything."""

    def filter(self, record):
        return False
