from setuptools import setup, find_packages

setup(
    name='erawan',
    version='0.0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'erawan = erawan.__main__:entrypoint_main'
        ]
    },
)
