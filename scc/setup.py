from setuptools import setup

setup(
    name='Student Counselling Cell Website',
    version='1.0',
    packages=['scc'],
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
)