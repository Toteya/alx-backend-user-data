#!/usr/bin/env python3
"""
filtered_logger:
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns log message obfuscated"""
    for field in fields:
        pattern = r';{}?(.*?);'.format(field)
        message = re.sub(pattern, ';{}={};'.format(field, redaction), message)
    return message
