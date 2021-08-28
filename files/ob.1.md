% OB(1) OB version 123
% Bart Thate 
% Aug 2021

# NAME

**OB** - python3 object library

# SYNOPSIS

ob \<cmd\> \[options\] \[key=value\] \[key==value\] 

# DESCRIPTION

**OB** provides a library (the ob package) you can use to program
objects under python3, an Object class, that mimics a dict while
using  attribute access and provides a save/load to/from json files
on disk. objects can be searched with database functions and uses
read-only files to improve persistence and a type in filename for
reconstruction.

    | grep print ob
    | grep __import__ ob
    | grep popen ob
    | grep exec ob
    | grep importlib ob


**OB** is also a IRC bot that can run as a  background
daemon for 24/7 a day presence in a IRC channel. You can use it to
display RSS feeds, act as a UDP to IRC gateway, program your own
commands for it and have it log objects on disk to search them. 

# INSTALL

| pip3 install ob
| systemctl enable ob \-\-now

| * default channel/server is #ob on localhost

# CONFIGURATION

| obc cfg server=\<server\> channel=\<channel\> nick=\<nick\> 

| obc cfg users=True
| obc met \<userhost\>

| obc pwd \<nickservnick\> \<nickservpass\>
| obc cfg password=\<outputfrompwd\>

| obc rss \<url\>

# PROGRAMMING

basic usage is this.

    >>> from ob.obj import Object
    >>> o = Object()
    >>> o.key = "value"
    >>> o.key
    'value'

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

the obj.py module has the basic methods like load/save to disk providing bare
persistence.

    >>> from ob.obj import Object, load, save, setwd
    >>> setwd("data")
    >>> o = Object()
    >>> o["key"] = "value"
    >>> p = save(o)
    >>> p
    'ob.obj.Object/4b58abe2-3757-48d4-986b-d0857208dd96/....
    >>> oo = Object()
    >>> load(oo, p)
    >> oo.key
    'value'

great for giving objects peristence by having their state stored in files.

# COPYRIGHT

**OB** is placed in the Public Domain, no Copyright, no LICENSE.

# AUTHOR

Bart Thate 

# SEE ALSO

https://pypi.org/project/ob

