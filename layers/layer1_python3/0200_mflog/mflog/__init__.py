# -*- coding: utf-8 -*-

import os
import logging
import logging.config
import json
from jinja2 import Template

MFLOG_DEFAULT_CONFIG_PATH = \
    os.path.join(os.environ.get('MFCOM_HOME', ''), "config",
                 "python_default_logging.json")
MFLOG_CONFIG_PATH = \
    os.path.join(os.environ.get('MODULE_HOME', ''), "config",
                 "python_logging.json")
MODULE = os.environ.get('MODULE')
MODULE_LOG_DEFAULT_LEVEL_VAR = "%s_LOG_DEFAULT_LEVEL" % MODULE
MODULE_LOG_STDOUT_VAR = "%s_LOG_STDOUT" % MODULE
MODULE_LOG_STDERR_VAR = "%s_LOG_STDERR" % MODULE
MODULE_LOG_EXTERNAL_MONITORING_FILE_VAR = \
    "%s_LOG_EXTERNAL_MONITORING_FILE" % MODULE
MODULE_LOG_EXTERNAL_MONITORING_LEVEL_VAR = \
    "%s_LOG_EXTERNAL_MONITORING_LEVEL" % MODULE
MODULE_LOG_EXTERNAL_MONITORING_FORMATTER_VAR = \
    "%s_LOG_EXTERNAL_MONITORING_FORMATTER" % MODULE


def __get_jinja2_env():
    module_log_default_level = \
        os.environ.get(MODULE_LOG_DEFAULT_LEVEL_VAR,
                       'NOTSET')
    module_log_stdout = os.environ.get(MODULE_LOG_STDOUT_VAR,
                                       'ext://sys.stdout')
    module_log_stderr = os.environ.get(MODULE_LOG_STDERR_VAR,
                                       'ext://sys.stderr')
    module_log_em_file = \
        os.environ.get(MODULE_LOG_EXTERNAL_MONITORING_FILE_VAR, "null")
    module_log_em_level = \
        os.environ.get(MODULE_LOG_EXTERNAL_MONITORING_LEVEL_VAR, "CRITICAL")
    module_log_em_formatter = \
        os.environ.get(MODULE_LOG_EXTERNAL_MONITORING_FORMATTER_VAR, "metwork")
    jinja2_env = {
        'MODULE_LOG_DEFAULT_LEVEL': module_log_default_level,
        'MODULE_LOG_STDOUT': module_log_stdout,
        'MODULE_LOG_STDERR': module_log_stderr,
        'MODULE_LOG_EXTERNAL_MONITORING_FILE': module_log_em_file,
        'MODULE_LOG_EXTERNAL_MONITORING_LEVEL': module_log_em_level,
        'MODULE_LOG_EXTERNAL_MONITORING_FORMATTER': module_log_em_formatter
    }
    jinja2_env.update(os.environ)
    return jinja2_env


def set_logging_config():
    """Set the metwork logging config.

    If the env var MFLOG_DEBUG_CONFIGURATION is set to 1,
    you have a debug output on stdout on the full configuration
    applied with logging.config.dictConfig.
    """
    with open(MFLOG_DEFAULT_CONFIG_PATH, 'r') as f:
        default_config_content = f.read()
    template = Template(default_config_content)
    jinja2_env = __get_jinja2_env()
    default_config_content = template.render(jinja2_env)
    overriden_config_content = '{}'
    try:
        with open(MFLOG_CONFIG_PATH, 'r') as f:
            overriden_config_content = f.read()
        template = Template(overriden_config_content)
        overriden_config_content = template.render(jinja2_env)
    except IOError:
        pass
    try:
        config_dict = json.loads(default_config_content)
    except ValueError:
        print("BAD DEFAULT LOGGING CONFIG")
        os._exit(3)
    try:
        overriden_config = json.loads(overriden_config_content)
    except ValueError:
        print("BAD LOGGING CONFIG")
        os._exit(3)
    for key in ('formatters', 'handlers', 'loggers', 'filters'):
        try:
            config_dict[key].update(overriden_config[key])
        except Exception:
            pass
    if int(os.environ.get('MFLOG_DEBUG_CONFIGURATION', '0')) == 1:
        print("WE ARE GOING TO SET PYTHON LOGGING CONFIGURATION:")
        print("=================================================")
        print(json.dumps(config_dict, indent=4))
        print("=================================================")
    logging.config.dictConfig(config_dict)


# IMPORTANT LINE : set logging config at import
set_logging_config()


def getLogger(*args, **kwargs):
    """Return a python logging logger.

    This function is just a wrapper.

    But by importing and using this one (and not directly logging.getLogger),
    you are sure that the logging config is set.
    """
    return logging.getLogger(*args, **kwargs)
