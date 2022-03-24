'''
Created on 30-Jul-2021

@author: deerakum
'''
import configparser
from dockerviolations.utils.general_util import get_resource_path


class PropertyUtil:
    def __init__(self, prop_file_name, section_name):
        self._prop_file_name = prop_file_name
        self._section_name = section_name

    def get_value_for_key(self, prop_key):
        config_load = self.get_config_parser_obj()
        return config_load.get(self._section_name, prop_key)

    def get_config_parser_obj(self):
        config_load = configparser.RawConfigParser()
        config_load.read(get_resource_path(self._prop_file_name))
        return config_load


def get_recommendation_from_prop(file_name, section_name, prop_key):
    prop_obj = PropertyUtil(file_name, section_name)
    return prop_obj.get_value_for_key(prop_key)
