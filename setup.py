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
    name='obot',
    version='101',
    description="24/7 channel daemon",
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    url='https://github.com/bthate67/obot',
    long_description=read(),
    license='Public Domain',
    package_dir={'': 'ob'},
    py_modules=mods("ob"),
    zip_safe=True,
    include_package_data=True,
    data_files=[('share/obot', ['files/obot.service']),
                ('share/man/man1', ['files/obot.1.gz'])],
    scripts=["bin/obot", "bin/obotd", "bin/ocmd", "bin/octl"],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
