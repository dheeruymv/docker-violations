'''
Created on 20-Nov-2021

@author: dheer
'''
from bin.dockerviolations.utils.general_util import is_number_exists
from dockerviolations.utils.property_util import get_recommendation_from_prop


class RuleEngine:
    def __init__(self, content_list):
        self._docker_content = content_list
        self._docker_prop_file = "docker_rule_recommendation.properties"
        self._rr_section = "RRSection"

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
                get_recommendation_from_prop(self._docker_prop_file,
                                             self._rr_section, 'mkdir_rule')
            })
        violations.append(self._get_label_violations())
        if self._check_sudo_presence():
            violations.append(self._get_sudo_violation())
        if self._check_add_presence():
            violations.append(self._get_add_violation())
        if self._check_base_image_violation():
            violations.append(self._get_base_image_violation())
        if self._check_for_dists():
            violations.append(self._get_dists_violation())
        if self._check_for_cd_cmd():
            violations.append(self._get_cd_cmd_violations())
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
                "Line #":
                self._get_line_number("LABEL"),
                "Violation":
                "LABEL command is not present",
                "Recommendation":
                get_recommendation_from_prop(self._docker_prop_file,
                                             self._rr_section,
                                             'label_not_present_rule')
            }
        elif label_counter > 1:
            return {
                "Line #":
                self._get_line_number("LABEL"),
                "Violation":
                "Multiple LABEL commands are present",
                "Recommendation":
                get_recommendation_from_prop(self._docker_prop_file,
                                             self._rr_section,
                                             'multiple_labels_rule')
            }

    def _get_label_counter(self):
        counter = 0
        for docker_command in self._docker_content:
            if "label".upper() in docker_command:
                counter += 1
        return counter

    def _get_line_number(self, pattern=None, regex=None):
        line_numbers = ""
        if pattern and not regex:
            for idx, content in enumerate(self._docker_content):
                if pattern in content:
                    line_numbers = line_numbers + "," + str(idx + 1)
            return line_numbers.lstrip(
                ","
            ) if line_numbers else "No Line containing the command in Docker file"
        # else:
        #     compiled_pattern = re.compile(pattern)
        #     for idx, content in enumerate(self._docker_content):
        #         if re.match(compiled_pattern, content):
        #             line_numbers = line_numbers + "," + str(idx + 1)
        #     return line_numbers.lstrip(
        #         ","
        #     ) if line_numbers else "No Line containing the command in Docker file"

    def _check_sudo_presence(self):
        return True if "SUDO" or "sudo" in self._docker_content else False

    def _check_add_presence(self):
        return True if "ADD" or "add" in self._docker_content else False

    def _get_sudo_violation(self):
        return {
            "Line #":
            self._get_line_number("sudo "),
            "Violation":
            "'sudo' found, Avoid installing!!",
            "Recommendation":
            get_recommendation_from_prop(self._docker_prop_file,
                                         self._rr_section, 'sudo_rule')
        }

    def _get_add_violation(self):
        return {
            "Line #":
            self._get_line_number("ADD "),
            "Violation":
            "ADD is not preferred for copying of file(s)",
            "Recommendation":
            get_recommendation_from_prop(self._docker_prop_file,
                                         self._rr_section, 'add_rule')
        }

    def _check_base_image_violation(self):
        base_image_line = [
            command for command in self._docker_content if "FROM" in command
        ][0]
        return True if ":" not in base_image_line and not is_number_exists(
            base_image_line) else False

    def _get_base_image_violation(self):
        return {
            "Line #":
            self._get_line_number("FROM "),
            "Violation":
            "Tag the version of image explicitly",
            "Recommendation":
            get_recommendation_from_prop(self._docker_prop_file,
                                         self._rr_section, 'base_image_rule')
        }

    def _check_for_dists(self):
        pip_install_cmds = [
            command for command in self._docker_content
            if "pip install" in command
        ]
        dists = [
            pip_install_cmd for pip_install_cmd in pip_install_cmds
            if ".tar.gz" or ".whl" in pip_install_cmd
        ]
        return True if dists else False

    def _get_dists_violation(self):
        return {
            "Line #":
            self._get_line_number(pattern=".tar.gz"),
            "Violation":
            "Dist files like .tar.gz/.whl shouldn't be copied",
            "Recommendation":
            get_recommendation_from_prop(self._docker_prop_file,
                                         self._rr_section, 'dist_rule')
        }

    def _check_for_cd_cmd(self):
        run_cd_cmds = [
            command for command in self._docker_content if "RUN cd" in command
        ]
        return True if run_cd_cmds else False

    def _get_cd_cmd_violations(self):
        return {
            "Line #":
            self._get_line_number(pattern="RUN cd"),
            "Violation":
            "Use WORKDIR, not cd",
            "Recommendation":
            get_recommendation_from_prop(self._docker_prop_file,
                                         self._rr_section, 'cd_workdir_rule')
        }
