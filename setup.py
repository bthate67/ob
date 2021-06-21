# This file is place in the Public Domain.

from setuptools import setup, os

def files(name):
    res = []
    for p in os.listdir(name):
        if p.startswith("__"):
            continue
        if p.endswith(".py"):
            res.append(os.path.join(name, p))
    return res

def mods(name):
    res = []
    for p in os.listdir(name):
        if p.startswith("__"):
            continue
        if p.endswith(".py"):
            res.append(p[:-3])
    return res

def read():
    return open("README.rst", "r").read()

setup(
    name='ob',
    version='100',
    description="python3 object library",
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    url='https://github.com/bthate67/ob',
    long_description=read(),
    license='Public Domain',
    package_dir={'': 'ob'},
    py_modules=mods("ob"),
    zip_safe=True,
    scripts=["bin/ob"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
