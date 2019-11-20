from setuptools import setup
import subprocess

setup(
    name='botani',
    version='0',
    packages=['botani'],
    license='MIT',
    author="Aapo Vienamo & Juuso Laine",
    author_email="aapo.vienamo@aalto.fi",
    long_description='Python script for measuring and sending plant moisture data to influxdb',
    entry_points = {
        'console_scripts': [
            'botani=botani.botani:main',
        ]
    },
    install_requires=['RPi.GPIO', 'influxdb'],
)
