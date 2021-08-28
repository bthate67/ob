# This file is place in the Public Domain.

import os

from setuptools import setup

def read():
    return open("README.rst", "r").read()

def uploadlist(dir):
    upl = []
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl

setup(
    name='ob',
    version='124',
    url='https://github.com/bthate/ob2',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="python3 object library",
    long_description=read(),
    license='Public Domain',
    packages=["ob"],
    zip_safe=True,
    scripts=["bin/ob", "bin/obt"],
    include_package_data=True,
    data_files=[
                ('lib/ob/mod', uploadlist("mod")),
                ('share/ob', ["files/ob.1.md"]),
                ('man/man1', ["files/ob.1.gz"])],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
