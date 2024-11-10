#!/usr/bin/env python3
"""
filtered_logger:
"""
import logging
import re
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        formatted_msg = logging.Formatter(self.FORMAT).format(record)
        return formatted_msg


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns log message obfuscated"""
    for field in fields:
        pattern = '{}=?(.*?){}'.format(field, separator)
        message = re.sub(pattern, '{}={}{}'.format(field, redaction,
                                                   separator), message)
    return message
