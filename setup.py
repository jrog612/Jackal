import os
import re

from setuptools import setup, find_packages


def read(f):
    return open(f, 'r', encoding='utf-8').read()


def get_version():
    init_py = open(os.path.join('jackal', '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name='django_jackal',
    version=get_version(),
    description='Boilerplate for Django and Django REST Framework',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    url='https://github.com/joyongjin/jackal',
    author='Yongjin Jo',
    author_email='wnrhd114@gmail.com',
    lisence='MIT',
    packages=find_packages(exclude=['tests*', '.*']),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'django>=2.0', 'djangorestframework', 'python-dateutil',
    ],
    python_requires='>=3.5'
)
