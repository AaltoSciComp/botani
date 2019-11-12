from setuptools import setup
import subprocess

try:
    systemd_service_path = subprocess.check_output(
        ['pkg-config', '--variable=systemdsystemunitdir', 'systemd']
    ).decode('utf-8').rstrip()
    systemd_service_data_file = [(systemd_service_path, ['botani.service'])]
except:
    print("NOTE: Could not determine systemd service file install path.")
    print("      Possibly either pkg-config or systemd is missing.")
    systemd_service_data_file = []

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
    data_files = [
        ('/etc/', ['botani-plants.conf', 'botani-influxdb.conf']),
    ] + systemd_service_data_file,
    install_requires=['RPi.GPIO', 'influxdb'],
)
