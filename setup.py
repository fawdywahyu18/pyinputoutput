# Setup for strctural check IRIO

from setuptools import setup

setup(
    name='structural_check_IRIO',
    version='0.1.0',
    py_modules=['structural_check_IRIO'],
    install_requires=[
        'et-xmlfile==1.1.0',
        'numpy==1.23.5',
        'openpyxl==3.0.10',
        'pandas==1.5.2',
        'python-dateutil==2.8.2',
        'pytz==2023.3',
        'six==1.16.0',
    ],
    entry_points='''
        [console_scripts]
        structural_check_IRIO=structural_check_IRIO:structural_check_IRIO
    ''',
)

