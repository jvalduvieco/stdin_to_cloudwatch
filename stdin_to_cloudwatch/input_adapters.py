import re
import logging

logger = logging.getLogger()


def decide_input_adapter(adapter_name):
    return adapt_django_logs if adapter_name == 'django' else adapt_doing_nothing


def adapt_doing_nothing(line):
    return line


def adapt_django_logs(line):
    try:
        matches = re.match(r'^\[.+\] \w+ (.+)$', line)
        if matches:
            return matches.groups()[0]
        else:
            return line
    except Exception as err:
        logger.error("Parse input. Error: %s" % err.message)
