import os
import tempfile
from unittest import TestCase
from mflog import getLogger, set_logging_config


def get_logger(*args, **kwargs):
    os.environ['MFCOM_LOG_STDERR'] = '/dev/null'
    set_logging_config()
    return getLogger(*args, **kwargs)


class BasicTestCase(TestCase):

    def test_debug(self):
        x = get_logger("foo.bar")
        x.debug("debug message")

    def test_info(self):
        x = get_logger("foo.bar")
        x.info("info message")

    def test_warning(self):
        x = get_logger("foo.bar")
        x.warning("warning message")

    def test_critical(self):
        x = get_logger("foo.bar")
        x.critical("warning message")

    def test_error(self):
        x = get_logger("foo.bar")
        x.error("error message")

    def test_suffix(self):
        fh, tmp_filepath = tempfile.mkstemp()
        os.environ['METWORK_LOG_SUFFIX'] = 'test suffix'
        os.environ['MFCOM_LOG_STDOUT'] = tmp_filepath
        x = get_logger("foo.suffix")
        x.info("bar")
        os.close(fh)
        with open(tmp_filepath, 'r') as f:
            content = f.read()
        self.assertTrue("test suffix" in content)
        os.unlink(tmp_filepath)
