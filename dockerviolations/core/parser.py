'''
Created on 19-Sep-2021

@author: deerakum
'''
from dockerviolations.utils.logger_util import LoggerUtil
from dockerviolations.core.ruleengine import RuleEngine

logger = LoggerUtil().get_logger()


class Parser:
    def __init__(self, content):
        self._content = content

    def parse_for_violations(self):
        content_list = self._content.split("\n")
        violations = RuleEngine(content_list).get_violations()
        return violations
