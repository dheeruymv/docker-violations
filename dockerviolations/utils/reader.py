'''
Created on 17-Sep-2021

@author: deerakum
'''


class FileReader:
    def __init__(self):
        self._content = ""

    def get_content(self, file_name):
        with open(file_name, 'r') as docker_file_reader:
            return docker_file_reader.read()
