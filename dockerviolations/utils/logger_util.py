'''
Created on 30-Jul-2021

@author: deerakum
'''
import logging
import sys
from dockerviolations.utils.property_util import PropertyUtil


class LoggerUtil:
    def get_logger(self):
        #log_level_from_prop = PropertyUtil("logger.properties", "LoggerSection").get_value_for_key("loglevel")
        log_level = "INFO"
        if log_level == "DEBUG":
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        else:
            logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        return logging
