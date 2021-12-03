'''
Created on 20-Nov-2021

@author: dheer
'''


class RuleEngine:
    def __init__(self, content_list):
        self._docker_content = content_list
        self._docker_rules = {
            'mkdir_rule':
            "Group all 'mkdir' commands into single layer",
            'label_not_present_rule':
            "Use LABEL Command to organize images by project, recording license info, to aid in automation",
            'multiple_labels_rule':
            "If docker version < 1.10: Merge multiple LABEL commands to single LABEL command. If docker version >=1.10: ignore the recommendation, but as good practice merge LABEL to single command",
            "sudo_rule":
            "Avoid installing (or) using 'sudo' as it has unpredictable TTY and signal-forwarding behaviour, use 'gosu' (https://github.com/tianon/gosu) ",
            "add_rule":
            "COPY is preferred as copy does the basic copy which is transparent than ADD",
            "base_image_rule":
            "Tag the version of the image explicitly, never rely on 'latest' as tag"
        }

    def get_violations(self):
        ''' Returns the violations like 
        Line #, Violation String, Recommendation'''
        violations = []
        if self._is_multiple_mkdir_present():
            violations.append({
                "Line #":
                self._get_line_number("mkdir"),
                "Violation":
                "MKDIR command can be improved",
                "Recommendation":
                self._docker_rules['mkdir_rule']
            })
        violations.append(self._get_label_violations())
        if self._check_sudo_presence():
            violations.append(self._get_sudo_violation())
        if self._check_add_presence():
            violations.append(self._get_add_violation())
        if self._check_base_image_violation():
            violations.append(self._get_base_image_violation())
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
                "Recommendation": self._docker_rules['label_not_present_rule']
            }
        elif label_counter > 1:
            return {
                "Line #": self._get_line_number("LABEL"),
                "Violation": "Multiple LABEL commands are present",
                "Recommendation": self._docker_rules['multiple_labels_rule']
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
                line_numbers = line_numbers + "," + str(idx + 1)
        return line_numbers.lstrip(
            ","
        ) if line_numbers else "No Line containing the command in Docker file"

    def _check_sudo_presence(self):
        return True if "SUDO" or "sudo" in self._docker_content else False

    def _check_add_presence(self):
        return True if "ADD" or "add" in self._docker_content else False

    def _get_sudo_violation(self):
        return {
            "Line #": self._get_line_number("sudo "),
            "Violation": "'sudo' found, Avoid installing!!",
            "Recommendation": self._docker_rules['sudo_rule']
        }

    def _get_add_violation(self):
        return {
            "Line #": self._get_line_number("ADD "),
            "Violation": "ADD is not preferred for copying of file(s)",
            "Recommendation": self._docker_rules['add_rule']
        }

    def _check_base_image_violation(self):
        base_image_line = [
            command for command in self._docker_content if "FROM" in command
        ][0]
        return True if ":" not in base_image_line else False

    def _get_base_image_violation(self):
        return {
            "Line #": self._get_line_number("FROM "),
            "Violation": "Tag the version of image explicitly",
            "Recommendation": self._docker_rules['base_image_rule']
        }
