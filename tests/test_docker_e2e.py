'''
Created on 18-Dec-2021

@author: dheer
'''
import unittest
import sys
from dockerviolations.__main__ import main
from dockerviolations.utils.general_util import get_resource_path


class TestDockerViolation(unittest.TestCase):
    def test_docker_violations_e2e(self):
        sys.argv[1] = get_resource_path("sample_dockerfile")
        actual = main()
        print("Actual has ", actual)
        expected = [{
            'Line #':
            '60,72',
            'Violation':
            'MKDIR command can be improved',
            'Recommendation':
            "Group all 'mkdir' commands into single layer"
        }, {
            'Line #':
            'No Line containing the command in Docker file',
            'Violation':
            'LABEL command is not present',
            'Recommendation':
            'Use LABEL Command to organize images by project, recording license info, to aid in automation'
        }, {
            'Line #':
            '27',
            'Violation':
            "'sudo' found, Avoid installing!!",
            'Recommendation':
            "Avoid installing (or) using 'sudo' as it has unpredictable TTY and signal-forwarding behaviour, use 'gosu' (https://github.com/tianon/gosu)"
        }, {
            'Line #':
            '61',
            'Violation':
            'ADD is not preferred for copying of file(s)',
            'Recommendation':
            'COPY is preferred. As copy does the basic copy which is transparent than ADD'
        }, {
            'Line #':
            '6',
            'Violation':
            'Tag the version of image explicitly',
            'Recommendation':
            "Tag the version of the image explicitly, never rely on 'latest' as tag"
        }, {
            'Line #':
            '80,88',
            'Violation':
            "Dist files like .tar.gz/.whl shouldn't be copied",
            'Recommendation':
            "Dist files like .tar.gz/.whl should be installed directly from the internal private repo's to decrease size of docker image"
        }, {
            'Line #':
            '71',
            'Violation':
            'Use WORKDIR, not cd',
            'Recommendation':
            'Rather than proliferating instructions like RUN cd.. && do-something, use WORKDIR. Use WORKDIR for Clarity and reliability.'
        }]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
