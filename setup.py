from setuptools import setup

requirements = [l.strip() for l in open('requirements.txt').readlines()]

setup(
    name='docker-violations',
    version='0.1',
    description='Docker Violations Tool',
    license="Proprietary",
    classifiers=['License :: Other/Proprietary License'],
    packages=['docker-violations'],
    install_requires=requirements,
    include_package_data=True,
    test_suite="tests",
)
