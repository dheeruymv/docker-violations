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
            'mkdir':
            "Group all 'mkdir' commands into single layer",
            'label_not_present':
            "Use LABEL Command to organize images by project, recording license info, to aid in automation",
            'multiple_labels':
            "If docker version < 1.10: Merge multiple LABEL commands to single LABEL command. If docker version >=1.10: ignore the recommendation, but as good practice merge LABEL to single command"
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
        violations.append(self._get_label_violations())
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

    def _get_label_violations(self):
        label_counter = self._get_label_counter()
        if label_counter == 0:
            return {
                "Line #": self._get_line_number("LABEL"),
                "Violation": "LABEL command is not present",
                "Recommendation": self._docker_rules['label_not_present']
            }
        elif label_counter > 1:
            return {
                "Line #": self._get_line_number("LABEL"),
                "Violation": "Multiple LABEL commands are present",
                "Recommendation": self._docker_rules['multiple_labels']
            }

    def _get_label_counter(self):
        counter = 0
        for docker_command in self._docker_content:
            if "label".upper() in docker_command:
                counter += 1
        return counter

    def _get_line_number(self, pattern):
        line_numbers = ""
        for idx, content in enumerate(self._docker_content):
            if pattern in content:
                line_numbers = line_numbers + " " + str(idx + 1)
        return line_numbers if line_numbers else "No Line containing the command in Docker file"
