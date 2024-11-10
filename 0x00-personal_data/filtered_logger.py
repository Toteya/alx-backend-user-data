#!/usr/bin/env python3
"""
filtered_logger:
"""
import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        record.msg = record.msg.replace(';', '; ')
        return logging.Formatter(self.FORMAT).format(record).strip()


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns log message obfuscated"""
    for field in fields:
        pattern = '{}=?(.*?){}'.format(field, separator)
        message = re.sub(pattern, '{}={}{}'.format(field, redaction,
                                                   separator), message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a logging.Logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler
    stream_handler.setFormatter(RedactingFormatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to a database
    """
    db_connection = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD'),
        host=os.getenv('PERSONAL_DATA_DB_HOST'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connection
