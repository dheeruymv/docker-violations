'''
Created on 19-Sep-2021

@author: deerakum
'''
from dockerviolations.utils.logger_util import LoggerUtil

logger = LoggerUtil().get_logger()


class Parser:
    def __init__(self, content):
        self._content = content

    def parse_for_violations(self):
        content_list = self._content.split("\n")
        violations = RuleEngine(content_list).get_violations()
        return violations


class RuleEngine:
    def __init__(self, content_list):
        self._docker_content = content_list
        self._docker_rules = {
            'mkdir': "Group all 'mkdir' commands into single layer"
        }

    def get_violations(self):
        ''' Returns the violations like 
        Line #, Violation String, Recommendation'''
        violations = []
        if self._is_multiple_mkdir_present():
            violations.append({
                "Line #": self._get_line_number("mkdir"),
                "Violation": "MKDIR command can be improved",
                "Recommendation": self._docker_rules['mkdir']
            })
        return violations

    def _is_entrypoint_or_cmd_present(self):
        if "ENTRYPOINT" or "CMD" in self._docker_content:
            return True
        else:
            return False

    def _is_multiple_mkdir_present(self):
        counter = 0
        for docker_command in self._docker_content:
            if "mkdir" in docker_command:
                counter += 1
        return True if counter > 1 else False

    def _get_line_number(self, pattern):
        line_numbers = ""
        for idx, content in enumerate(self._docker_content):
            if pattern in content:
                line_numbers = line_numbers + " " + str(idx + 1)
        return line_numbers
