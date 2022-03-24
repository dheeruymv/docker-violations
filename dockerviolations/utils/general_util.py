'''
Created on 30-Jul-2021

@author: deerakum
'''
from pathlib import Path


def get_resource_path(relative_path_to_resources):
    under_test = True
    self_pathname = Path(__file__)
    util_pathname = self_pathname.parent
    dockerviolations_pathname = util_pathname.parent
    main_project_path = dockerviolations_pathname.parent
    if under_test:
        resources_pathname = main_project_path / "tests" / "resources"
    else:
        resources_pathname = main_project_path / "resources"
    pathname = resources_pathname / relative_path_to_resources
    return pathname.resolve()


def is_number_exists(inp_str):
    is_num_exists = False
    for char in inp_str:
        if char.isdigit():
            is_num_exists = True
    return is_num_exists
