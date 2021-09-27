'''
Created on 30-Jul-2021

@author: deerakum
'''
from pathlib import Path


def get_resource_path(relative_path_to_resources):
    self_pathname = Path(__file__)
    util_pathname = self_pathname.parent
    collectors_pathname = util_pathname.parent
    healthmonitoring_pathname = collectors_pathname.parent
    tests_pathname = healthmonitoring_pathname.parent
    print("test has ", tests_pathname)
    project_pathname = tests_pathname.parent
    resources_pathname = project_pathname / "resources"
    pathname = resources_pathname / relative_path_to_resources
    return pathname.resolve()
