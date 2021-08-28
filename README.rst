README
######

NAME
====

**OB** - python3 object library

SYNOPSIS
========

ob \<cmd\> \[options\] \[key=value\] \[key==value\] 

DESCRIPTION
===========

OB is a pure python3 object library that can be used to program objects.
 
The ob package provides a library you can use to program objects 
under python3. It provides a basic Object, that mimics a dict while using 
attribute access and provides a save/load to/from json files on disk. objects
can be searched with a little database module, it uses read-only files to
improve persistence and a type in filename for reconstruction.

Basic usage is this.

    >>> from ob.obj import Object
    >>> o = Object()
    >>> o.key = "value"
    >>> o.key
    'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

The obj.py module has the basic methods like load/save to disk providing bare
persistence.

    >>> from ob.obj import Object, load, save, setwd
    >>> setwd("data")
    >>> o = Object()
    >>> o["key"] = "value"
    >>> p = save(o)
    >>> p
    'ob.obj.Object/4b58abe2-3757-48d4-986b-d0857208dd96/2021-04-12/21:15:33.734994
    >>> oo = Object()
    >>> load(oo, p)
    >> oo.key
    'value'

Great for giving objects peristence by having their state stored in files.

INSTALL
=======

| sudo pip3 install ob
| sudo ob skl 
| ob mod=mod.irc

| * default channel/server is #ob on localhost

CONFIGURATION
==============

| ob cfg server=\<server\> channel=\<channel\> nick=\<nick\> 

| ob cfg users=True
| ob met \<userhost\>

| ob pwd \<nickservnick\> \<nickservpass\>
| ob cfg password=\<outputfrompwd\>

| ob rss \<url\>


FILES
=====

| bin/ob
| ~/.ob
| man/man1/ob.1.gz


COPYRIGHT
=========

**OB** is placed in the Public Domain, no Copyright, no LICENSE.

AUTHOR
======

Bart Thate 

SEE ALSO
========

https://pypi.org/project/ob
