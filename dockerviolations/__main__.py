'''
Created on 30-Jul-2021

@author: deerakum
'''
from dockerviolations.utils.logger_util import LoggerUtil
from dockerviolations.utils.reader import FileReader
from dockerviolations.core.parser import Parser
from dockerviolations.core.generator import Generator
import sys
from pathlib import Path

logger = LoggerUtil().get_logger()


def main():
    docker_file_path = sys.argv[1]
    logger.info("Processing the docker file '%s'", Path(docker_file_path).name)
    DockerViolations(docker_file_path).run()


class DockerViolations:
    def __init__(self, file_name):
        self._file_name = file_name

    def run(self):
        content = FileReader().get_content(self._file_name)
        violations = Parser(content).parse_for_violations()
        logger.info("Violations in main has %s", violations)
        #Generator(violations).generate_report()


if __name__ == '__main__':
    main()
